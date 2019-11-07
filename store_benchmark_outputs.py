import os
from datetime import datetime

import requests
from google.cloud import storage


class GoogleCloudStorage:
    def __init__(self, bucket_name):
        client = storage.Client()
        self.bucket = client.get_bucket(bucket_name)

    def upload_files(self, output_files, directory, **kwargs):
        date_string = datetime.utcnow().isoformat()

        for file in output_files:
            blob = self.bucket.blob(f'{directory}/{date_string}/{file}')
            blob.metadata = {**kwargs}
            blob.upload_from_filename(filename=file)


def get_runner_version(runner_url):
    response = requests.get(f'{runner_url}/status')
    if response.status_code == 200:
        return response.json().get('version', '').strip()

    return None

'''
This script allows the upload of the benchmark outputs to a GCS Bucket.
If running locally, you must specify valid Application Default Credentials (ADC):
https://cloud.google.com/docs/authentication/production
'''
if __name__ == '__main__':
    gcs_bucket_name = os.getenv('GCS_OUTPUT_BUCKET')
    if gcs_bucket_name:
        host = os.getenv('HOST')
        locust_options = os.getenv('LOCUST_OPTS')
        requests_json = os.getenv('REQUESTS_JSON')
        output_directory = os.getenv('OUTPUT_DIRECTORY')
        min_wait = os.getenv('USER_WAIT_TIME_MIN_SECONDS')
        max_wait = os.getenv('USER_WAIT_TIME_MAX_SECONDS')
        runner_version = get_runner_version(host)
        try:
            gcs = GoogleCloudStorage(bucket_name=gcs_bucket_name)
            gcs.upload_files(
                output_files=('output_requests.csv', 'output_distribution.csv'),
                directory=output_directory,
                host=host,
                min_wait=min_wait,
                max_wait=max_wait,
                requests_json=requests_json,
                locust_options=locust_options,
                runner_version=runner_version,
            )
        except Exception as ex:
            raise Exception(f"Error occurred during file upload to GCS - {ex}")
    else:
        raise Exception('GCS Bucket not specified by `GCS_OUTPUT_BUCKET`')