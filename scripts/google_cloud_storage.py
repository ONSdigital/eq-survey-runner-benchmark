import os
import json

from datetime import datetime, timedelta
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

    def get_files(self, number_of_days):
        output_dir = "outputs"

        for blob in self.client.list_blobs(self.bucket_name):
            blob_date = blob.name.split("/")[1].split("T")[0]

            from_date = (
                (datetime.utcnow() - timedelta(days=number_of_days)) if number_of_days else None
            )

            if from_date and datetime.strptime(blob_date, "%Y-%m-%d") < from_date:
                continue

            file_path = blob.name.rsplit('/', 1)[0]

            output_file_path = f'{output_dir}/{file_path}'

            if not os.path.exists(output_file_path):
                os.makedirs(output_file_path)

            blob.download_to_filename(filename=f'{output_dir}/{blob.name}')

            metadata_file_path = f"{output_dir}/{file_path}/metadata.json"
            if not os.path.exists(metadata_file_path):
                with open(metadata_file_path, 'w+') as file:
                    file.write(json.dumps(blob.metadata, indent=2))
