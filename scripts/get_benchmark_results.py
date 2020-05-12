import os
import sys

from scripts.google_cloud_storage import GoogleCloudStorage

if __name__ == '__main__':
    output_bucket = os.getenv("OUTPUT_BUCKET")

    if not output_bucket:
        print("'OUTPUT_BUCKET' environment variable must be provided")
        sys.exit(1)

    gcs = GoogleCloudStorage(bucket_name=output_bucket)
    print("Fetching files...")

    gcs.get_files()
    print('All files downloaded')
