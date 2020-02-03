import os

from scripts.google_cloud_storage import GoogleCloudStorage


if __name__ == '__main__':

    gcs_bucket_name = os.environ['GCS_OUTPUT_BUCKET']

    if not gcs_bucket_name:
        raise ValueError(
            'Value for `GCS_OUTPUT_BUCKET` environment variable not valid.'
        )

    gcs = GoogleCloudStorage(bucket_name=gcs_bucket_name)
    print("Fetching files...")
    gcs.get_files()

    print('All files downloaded')
