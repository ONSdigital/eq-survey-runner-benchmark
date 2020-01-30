import os

from scripts.google_cloud_storage import GoogleCloudStorage


if __name__ == '__main__':
    output_dir = "outputs"

    gcs_bucket_name = os.environ['GCS_OUTPUT_BUCKET']

    if not gcs_bucket_name:
        raise ValueError(
            'Value for `GCS_OUTPUT_BUCKET` environment variable not valid.'
        )

    application_credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    if not application_credentials:
        raise ValueError(
            'Value for `GOOGLE_APPLICATION_CREDENTIALS` environment variable not valid.'
        )

    gcs = GoogleCloudStorage(bucket_name=gcs_bucket_name)
    print("Fetching files...")
    gcs.get_files(output_dir)

    print('All files downloaded')
