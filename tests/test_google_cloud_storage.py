import pytest

from scripts.google_cloud_storage import GoogleCloudStorage


@pytest.fixture
def patch_gcs_client(mocker):
    return mocker.patch("scripts.google_cloud_storage.storage.Client")


def test_upload_files(patch_gcs_client):
    gcs_storage = GoogleCloudStorage(bucket_name="benchmark_bucket")

    gcs_storage.upload_files(
        output_files=["mock_output_stats.csv"], directory="benchmark_outputs"
    )

    bucket = patch_gcs_client.return_value.get_bucket.return_value
    blob = bucket.blob.return_value

    assert blob.upload_from_filename.call_count == 1
    assert blob.upload_from_filename.call_args[1] == {
        "filename": "mock_output_stats.csv"
    }


def test_upload_files_with_prefix(patch_gcs_client):
    gcs_storage = GoogleCloudStorage(bucket_name="benchmark_bucket")

    gcs_storage.upload_files(
        output_files=["mock_output_stats.csv"],
        directory="benchmark_outputs",
        output_filename_prefix="test",
    )

    bucket = patch_gcs_client.return_value.get_bucket.return_value
    blob = bucket.blob.return_value

    assert blob.upload_from_filename.call_count == 1
    assert blob.upload_from_filename.call_args[1] == {
        "filename": "mock_output_stats.csv"
    }
