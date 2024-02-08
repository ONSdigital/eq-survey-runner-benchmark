from scripts.get_aggregated_summary import get_results
from tests.conftest import (
    EXPECTED_OUTPUT_MULTIPLE_FOLDERS,
    EXPECTED_OUTPUT_SINGLE_FOLDER,
)


def test_get_aggregated_summary_single_folder():
    results = get_results(folders=["./tests/mock_stats/2024-02-07T03:09:41"])
    assert str(results) == EXPECTED_OUTPUT_SINGLE_FOLDER


def test_get_aggregated_summary_multiple_folders():
    results = get_results(
        folders=[
            "./tests/mock_stats/2024-02-07T03:09:41",
            "./tests/mock_stats/2024-02-06T03:09:41",
        ]
    )
    assert str(results) == EXPECTED_OUTPUT_MULTIPLE_FOLDERS
