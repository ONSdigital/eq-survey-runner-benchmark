import pytest

from scripts.benchmark_stats import BenchmarkStats
from tests.conftest import (
    EXPECTED_OUTPUT_MULTIPLE_FOLDERS,
    EXPECTED_OUTPUT_SINGLE_FOLDER, EXPECTED_OUTPUT_MULTIPLE_FOLDERS_WITH_PDF, EXPECTED_OUTPUT_SINGLE_FOLDER_WITH_PDF,
)


@pytest.fixture
def benchmark_stats():
    return BenchmarkStats(folder_paths=["./tests/mock_stats/2024-02-07T03:09:41"])


@pytest.fixture
def benchmark_stats_pdf():
    return BenchmarkStats(folder_paths=["./tests/mock_stats/2024-07-25T03:09:41"])


@pytest.fixture
def benchmark_stats_multiple():
    return BenchmarkStats(
        folder_paths=[
            "./tests/mock_stats/2024-02-07T03:09:41",
            "./tests/mock_stats/2024-02-06T03:09:41",
        ]
    )

@pytest.fixture
def benchmark_stats_multiple_with_pdf():
    return BenchmarkStats(
        folder_paths=[
            "./tests/mock_stats/2024-02-07T03:09:41",
            "./tests/mock_stats/2024-02-06T03:09:41",
            "./tests/mock_stats/2024-07-25T03:09:41",
            "./tests/mock_stats/2024-07-29T03:09:41",
        ]
    )


@pytest.mark.parametrize(
    "benchmark_stats_fixture, expected_result",
    (
        ("benchmark_stats", EXPECTED_OUTPUT_SINGLE_FOLDER),
        ("benchmark_stats_pdf", EXPECTED_OUTPUT_SINGLE_FOLDER_WITH_PDF),
        ("benchmark_stats_multiple", EXPECTED_OUTPUT_MULTIPLE_FOLDERS),
        ("benchmark_stats_multiple_with_pdf", EXPECTED_OUTPUT_MULTIPLE_FOLDERS_WITH_PDF)
    ),
)
def test_formatted_percentile(benchmark_stats_fixture, expected_result, request):
    assert str(request.getfixturevalue(benchmark_stats_fixture)) == expected_result


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


def test_pdf_percentile(benchmark_stats_pdf):
    assert benchmark_stats_pdf.pdf_percentile == 4700


def test_non_applicable_pdf_percentile(benchmark_stats):
    assert benchmark_stats.pdf_percentile == "N/A"


def test_session_percentile(benchmark_stats_pdf):
    assert benchmark_stats_pdf.session_percentile == 180
