import os
import sys

from scripts.google_cloud_storage import GoogleCloudStorage

if __name__ == '__main__':
    output_bucket = os.getenv("OUTPUT_BUCKET")

    days = os.getenv("NUMBER_OF_DAYS")
    if days and days.isdigit() is False:
        print("'NUMBER_OF_DAYS' environment variable must be a valid integer value")
        sys.exit(1)

    days = int(days) if days else None

    if not output_bucket:
        print("'OUTPUT_BUCKET' environment variable must be provided")
        sys.exit(1)

    gcs = GoogleCloudStorage(bucket_name=output_bucket)
    print("Fetching files...")

    gcs.get_files(number_of_days=days)
    print('All files downloaded')
