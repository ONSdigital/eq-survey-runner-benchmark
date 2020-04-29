import os
from datetime import datetime

import requests
from scripts.google_cloud_storage import GoogleCloudStorage


def get_runner_version(runner_url):
    response = requests.get(f'{runner_url}/status')
    if response.status_code == 200:
        return response.json().get('version', '').strip()


'''
This script allows the upload of the benchmark outputs to a GCS Bucket.
If running locally, you must specify valid Application Default Credentials (ADC):
https://cloud.google.com/docs/authentication/production
'''
if __name__ == '__main__':
    gcs_bucket_name = os.environ['GCS_OUTPUT_BUCKET']

    if not gcs_bucket_name:
        raise ValueError(
            'Value for `GCS_OUTPUT_BUCKET` environment variable not valid.'
        )

    host = os.getenv('HOST')
    runner_version = get_runner_version(host)
    locust_options = os.getenv('LOCUST_OPTS')
    requests_json = os.getenv('REQUESTS_JSON')
    output_directory = os.getenv('OUTPUT_DIRECTORY')
    min_wait = os.getenv('USER_WAIT_TIME_MIN_SECONDS')
    max_wait = os.getenv('USER_WAIT_TIME_MAX_SECONDS')
    filename_prefix = os.getenv('OUTPUT_FILENAME_PREFIX')

    gcs = GoogleCloudStorage(bucket_name=gcs_bucket_name)
    gcs.upload_files(
        output_files=(
            'output_stats.csv',
            'output_stats_history.csv',
            'output_failures.csv',
        ),
        directory=output_directory,
        output_filename_prefix=filename_prefix,
        host=host,
        min_wait=min_wait,
        max_wait=max_wait,
        requests_json=requests_json,
        locust_options=locust_options,
        runner_version=runner_version,
        timestamp=int(datetime.utcnow().timestamp()),
    )
