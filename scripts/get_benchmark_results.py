import os
import sys

from datetime import datetime, timedelta

from scripts.get_summary import parse_environment_variables
from scripts.google_cloud_storage import GoogleCloudStorage

if __name__ == '__main__':
    output_bucket = os.getenv("OUTPUT_BUCKET")

    parsed_variables = parse_environment_variables()
    number_of_days = parsed_variables['number_of_days']

    from_date = None

    if number_of_days:
        from_date = datetime.utcnow() - timedelta(days=number_of_days)

    if not output_bucket:
        print("'OUTPUT_BUCKET' environment variable must be provided")
        sys.exit(1)

    gcs = GoogleCloudStorage(bucket_name=output_bucket)
    print("Fetching files...")

    gcs.get_files(from_date=from_date)
    print('All files downloaded')
