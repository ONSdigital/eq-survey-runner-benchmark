import pytest
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from scripts.get_summary import get_results
from scripts.visualise_results import GraphGenerationFailed, get_data_frame, plot_data

expected_data_frame = DataFrame.from_dict(
    {"DATE": ["2024-02-07"], "50th": [58], "90th": [96], "95th": [173], "99th": [301]}
)

expected_data_frame_multiple_files = DataFrame.from_dict(
    {
        "DATE": ["2024-02-07", "2024-02-06"],
        "50th": [58, 58],
        "90th": [96, 99],
        "95th": [173, 177],
        "99th": [301, 319],
    }
)


def test_get_data_frame_single_file(get_results_single_file):
    dataframe = get_data_frame(get_results_single_file)
    assert_frame_equal(dataframe, expected_data_frame)


def test_get_data_frame_multiple_files():
    results = get_results(
        folders=[
            "./tests/mock_stats/2024-02-07T03:09:41",
            "./tests/mock_stats/2024-02-06T03:09:41",
        ]
    )
    dataframe = get_data_frame(results)
    assert_frame_equal(dataframe, expected_data_frame_multiple_files)


def test_plot_data_df(mocker, get_results_single_file):
    dataframe = get_data_frame(get_results_single_file)

    mock_plot_data = mocker.patch("scripts.visualise_results.plot_data")
    mock_plot_data(dataframe, 1)

    assert mock_plot_data.call_count == 1
    assert_frame_equal(mock_plot_data.call_args[0][0], expected_data_frame)


def test_plot_data(mocker, get_results_single_file):
    dataframe = get_data_frame(get_results_single_file)
    try:
        graph_output = mocker.patch("matplotlib.pyplot.savefig")
        plot_data(dataframe, 1)
        assert graph_output.call_count == 1
    except GraphGenerationFailed:
        pytest.fail("Graph generation failed")


def test_plot_data_failed():
    dataframe = DataFrame.from_dict({})
    with pytest.raises(GraphGenerationFailed):
        plot_data(dataframe, 1)
