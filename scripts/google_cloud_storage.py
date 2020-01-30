import os
import json

from google.cloud import storage


class GoogleCloudStorage:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket_name)

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

    def get_files(self, output_dir):
        for blob in self.client.list_blobs(self.bucket_name):

            file_path = '/'.join(iter(blob.name.split('/')[:2]))
            output_file_path = f'{output_dir}/{file_path}'
            if not os.path.exists(output_file_path):
                os.makedirs(output_file_path)

            blob.download_to_filename(filename=f'{output_dir}/{blob.name}')

            metadata_file = (
                f"{output_dir}/{file_path}/metadata.json"
            )
            with open(metadata_file, 'w+') as f:
                f.write(json.dumps(blob.metadata, indent=2))
