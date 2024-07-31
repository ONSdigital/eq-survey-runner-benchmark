import pytest

from scripts.get_summary import get_results

EXPECTED_OUTPUT_SINGLE_FOLDER = (
    '---\n'
    'Percentile Averages:\n'
    '50th: 58ms\n'
    '90th: 96ms\n'
    '95th: 173ms\n'
    '99th: 301ms\n'
    '99.9th: 477ms\n'
    '---\n'
    'GETs (99th): 380ms\n'
    'POSTs (99th): 211ms\n'
    '---\n'
    'PDF: N/A\n'
    'Session: 7600ms\n'
    '---\n'
    'Total Requests: 70,640\n'
    'Total Failures: 1\n'
    'Error Percentage: 0.0%\n'
)

EXPECTED_OUTPUT_SINGLE_FOLDER_WITH_PDF = (
    '---\n'
    'Percentile Averages:\n'
    '50th: 51ms\n'
    '90th: 75ms\n'
    '95th: 76ms\n'
    '99th: 76ms\n'
    '99.9th: 76ms\n'
    '---\n'
    'GETs (99th): 117ms\n'
    'POSTs (99th): 27ms\n'
    '---\n'
    'PDF: 4700ms\n'
    'Session: 180ms\n'
    '---\n'
    'Total Requests: 1,097\n'
    'Total Failures: 0\n'
    'Error Percentage: 0.0%\n'
)

EXPECTED_OUTPUT_MULTIPLE_FOLDERS = (
    '---\n'
    'Percentile Averages:\n'
    '50th: 58ms\n'
    '90th: 98ms\n'
    '95th: 176ms\n'
    '99th: 313ms\n'
    '99.9th: 595ms\n'
    '---\n'
    'GETs (99th): 383ms\n'
    'POSTs (99th): 234ms\n'
    '---\n'
    'PDF: N/A\n'
    'Session: 7300ms\n'
    '---\n'
    'Total Requests: 211,841\n'
    'Total Failures: 2\n'
    'Error Percentage: 0.0%\n'
)

EXPECTED_OUTPUT_MULTIPLE_FOLDERS_WITH_PDF = (
    '---\n'
    'Percentile Averages:\n'
    '50th: 58ms\n'
    '90th: 98ms\n'
    '95th: 175ms\n'
    '99th: 311ms\n'
    '99.9th: 589ms\n'
    '---\n'
    'GETs (99th): 380ms\n'
    'POSTs (99th): 232ms\n'
    '---\n'
    'PDF: 4850ms\n'
    'Session: 4504ms\n'
    '---\n'
    'Total Requests: 214,092\n'
    'Total Failures: 2\n'
    'Error Percentage: 0.0%\n'
)


@pytest.fixture
def get_results_single_file():
    return get_results(folders=["./tests/mock_stats/2024-02-07T03:09:41"])


@pytest.fixture
def get_results_single_file_with_pdf_endpoint():
    return get_results(folders=["./tests/mock_stats/2024-07-25T03:09:41"])


@pytest.fixture
def get_results_single_file_github():
    return get_results(folders=["./tests/mock_stats/2024-02-07T03:09:41"])
