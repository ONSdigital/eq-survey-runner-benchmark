import pytest

from scripts.benchmark_stats import BenchmarkStats
from tests.conftest import (
    EXPECTED_OUTPUT_MULTIPLE_FOLDERS,
    EXPECTED_OUTPUT_SINGLE_FOLDER,
)


@pytest.fixture
def benchmark_stats():
    return BenchmarkStats(folder_paths=["./tests/mock_stats/2024-02-07T03:09:41"])


@pytest.fixture
def benchmark_stats_multiple():
    return BenchmarkStats(
        folder_paths=[
            "./tests/mock_stats/2024-02-07T03:09:41",
            "./tests/mock_stats/2024-02-06T03:09:41",
        ]
    )


def test_formatted_percentiles(benchmark_stats):
    assert EXPECTED_OUTPUT_SINGLE_FOLDER == str(benchmark_stats)


def test_formatted_percentiles_multiple_folders(benchmark_stats_multiple):
    assert EXPECTED_OUTPUT_MULTIPLE_FOLDERS == str(benchmark_stats_multiple)


def test_files(benchmark_stats):
    assert benchmark_stats.files == [
        "./tests/mock_stats/2024-02-07T03:09:41/mock_output_stats.csv"
    ]


def test_percentiles(benchmark_stats):
    assert benchmark_stats.percentiles == {50: 58, 90: 96, 95: 173, 99: 301, 99.9: 477}


def test_total_requests(benchmark_stats):
    assert benchmark_stats.total_requests == 70640


def test_average_get(benchmark_stats):
    assert benchmark_stats.average_get == 380


def test_average_post(benchmark_stats):
    assert benchmark_stats.average_post == 211


def test_error_percentage(benchmark_stats):
    assert benchmark_stats.error_percentage == 0.0014156285390713476
