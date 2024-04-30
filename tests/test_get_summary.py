import pytest
from freezegun import freeze_time

from scripts.get_summary import get_results, parse_environment_variables
from tests.conftest import EXPECTED_OUTPUT_SINGLE_FOLDER

EXPECTED_OUTPUT_20240206_FOLDER = (
    '---\n'
    'Percentile Averages:\n'
    '50th: 58ms\n'
    '90th: 99ms\n'
    '95th: 177ms\n'
    '99th: 319ms\n'
    '99.9th: 654ms\n'
    '---\n'
    'GETs (99th): 384ms\n'
    'POSTs (99th): 245ms\n'
    '---\n'
    'Total Requests: 141,201\n'
    'Total Failures: 1\n'
    'Error Percentage: 0.0%\n'
)

EXPECTED_OUTPUT_20240206_FOLDER_GITHUB = (
    '{"body": "{'
    '**Benchmark Results**<br />'
    'Percentile Averages:<br />'
    '50th: 58ms< br/>'
    '90th: 96ms< br/>'
    '95th: 173ms< br/>'
    '99th: 301ms< br/>'
    '99.9th: 477ms<br />'
    'GETs (99th): 380ms<br />'
    'POSTs (99th): 211ms<br />'
    'Total Requests: 70,640<br />'
    'Total Failures: 1<br />'
    'Error Percentage: 0.0%<br />\n'
    '"}'
)


def test_get_results(get_results_single_file):
    results = list(get_results_single_file)
    assert str(results[0]) == f"2024-02-07\n{EXPECTED_OUTPUT_SINGLE_FOLDER}\n"


def test_get_results_github(get_results_single_file):
    results = list(
        get_results(
            folders=["./tests/mock_stats/2024-02-07T03:09:41"], output_to_github=True
        )
    )
    assert str(results[0]) == f"2024-02-07\n{EXPECTED_OUTPUT_20240206_FOLDER_GITHUB}"


def test_get_results_multiple_folders():
    generated_results = get_results(
        folders=[
            "./tests/mock_stats/2024-02-07T03:09:41",
            "./tests/mock_stats/2024-02-06T03:09:41",
        ]
    )
    results = list(generated_results)
    assert len(results) == 2
    assert str(results[0]) == f"2024-02-07\n{EXPECTED_OUTPUT_SINGLE_FOLDER}\n"
    assert str(results[1]) == f"2024-02-06\n{EXPECTED_OUTPUT_20240206_FOLDER}\n"


@freeze_time("2024-02-07T12:00:00")
def test_get_results_multiple_folders_with_number_of_days():
    generated_results = get_results(
        folders=[
            "./tests/mock_stats/2024-02-07T03:09:41",
            "./tests/mock_stats/2024-02-06T03:09:41",
        ],
        number_of_days=1,
    )

    # Number of days set to 1, so the 2024-02-06 folder should be ignored
    results = list(generated_results)
    assert len(results) == 1
    assert str(results[0]) == f"2024-02-07\n{EXPECTED_OUTPUT_SINGLE_FOLDER}\n"


def test_parse_environment_variables_with_valid_number_of_days(monkeypatch):
    monkeypatch.setenv("NUMBER_OF_DAYS", "10")
    monkeypatch.setenv("OUTPUT_DATE", "2024-02-07")
    monkeypatch.setenv("OUTPUT_DIR", "outputs")
    monkeypatch.setenv("OUTPUT_TO_GITHUB", "False")

    env_vars = parse_environment_variables()

    assert env_vars == {
        "number_of_days": 10,
        "output_date": "2024-02-07",
        "output_dir": "outputs",
        "output_to_github": "False",
    }


def test_parse_environment_variables_with_invalid_number_of_days(monkeypatch):
    monkeypatch.setenv("NUMBER_OF_DAYS", "test")

    with pytest.raises(SystemExit):
        parse_environment_variables()
