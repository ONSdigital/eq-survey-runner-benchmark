import json
import os

from google.cloud import storage


class GoogleCloudStorage:
    def __init__(self, bucket_name):
        client = storage.Client()
        self.bucket = client.get_bucket(bucket_name)
        self.blobs = client.list_blobs(bucket_name)

    def upload_files(
        self, output_files, directory, output_filename_prefix=None, **kwargs
    ):
        for output_file in output_files:
            output_filename = (
                f'{output_filename_prefix}_{output_file}'
                if output_filename_prefix
                else output_file
            )

            blob = self.bucket.blob(f'{directory or ""}/{output_filename}')
            blob.metadata = {**kwargs}
            blob.upload_from_filename(filename=output_file)

    def get_files(self):
        output_dir = 'outputs'
        for blob in self.blobs:

            blob = self.bucket.get_blob(blob.name)

            file_path = '/'.join(iter(blob.name.split('/')[:2]))
            output_file_path = f'{output_dir}/{file_path}'
            if not os.path.exists(output_file_path):
                os.makedirs(output_file_path)

            blob.download_to_filename(filename=f'{output_dir}/{blob.name}')

            metadata_file = (
                f"{output_dir}/{blob.name.replace('.csv', '-metadata.json')}"
            )
            with open(metadata_file, 'w+') as f:
                f.write(json.dumps(blob.metadata, indent=2))


if __name__ == '__main__':
    gcs_bucket_name = os.environ['GCS_OUTPUT_BUCKET']

    if not gcs_bucket_name:
        raise ValueError(
            'Value for `GCS_OUTPUT_BUCKET` environment variable not valid.'
        )

    application_credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    if not gcs_bucket_name:
        raise ValueError(
            'Value for `GOOGLE_APPLICATION_CREDENTIALS` environment variable not valid.'
        )

    gcs = GoogleCloudStorage(bucket_name=gcs_bucket_name)
    gcs.get_files()

    print('All files downloaded')

