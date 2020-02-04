import sys

from scripts.google_cloud_storage import GoogleCloudStorage


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Provide the bucket name as a parameter e.g. performance-test-outputs")
    else:
        gcs_bucket_name = sys.argv[-1]

        gcs = GoogleCloudStorage(bucket_name=gcs_bucket_name)
        print("Fetching files...")

        gcs.get_files()
        print('All files downloaded')
