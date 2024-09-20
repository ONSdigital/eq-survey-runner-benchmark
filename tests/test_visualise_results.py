from glob import glob

import pytest
from freezegun import freeze_time
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from scripts.get_summary import get_results
from scripts.visualise_results import (
    GraphGenerationFailed,
    create_graph,
    get_additional_metrics_data_frame,
    get_dataframes,
    get_performance_data_frame,
)

expected_performance_dataframe = DataFrame.from_dict(
    {"DATE": ["2024-02-07"], "50th": [58], "90th": [97], "95th": [174], "99th": [301]}
)

expected_pdf_session_dataframe = DataFrame.from_dict(
    {"DATE": ["2024-02-09"], "PDF": [4700], "Session": [180]}
)

expected_performance_dataframe_consecutive_days = DataFrame.from_dict(
    {
        "DATE": ["2024-02-07", "2024-02-06"],
        "50th": [58, 58],
        "90th": [97, 100],
        "95th": [174, 178],
        "99th": [301, 320],
    }
)

expected_pdf_session_dataframe_consecutive_days = DataFrame.from_dict(
    {
        "DATE": ["2024-02-09", "2024-02-12"],
        "PDF": [4700, 5000],
        "Session": [180, 440],
    }
)

expected_performance_dataframe_multiple_days = DataFrame.from_dict(
    {
        "DATE": ["2024-02-06", "2024-02-07", "2024-02-09", "2024-02-12"],
        "50th": [58, 58, 52, 45],
        "90th": [100, 97, 75, 75],
        "95th": [178, 174, 76, 79],
        "99th": [320, 301, 76, 80],
    }
)

expected_pdf_session_dataframe_multiple_days = DataFrame.from_dict(
    {
        "DATE": ["2024-02-06", "2024-02-07", "2024-02-09", "2024-02-12"],
        "PDF": [None, None, 4700, 5000],
        "Session": [7150, 7600, 180, 440],
    }
)

dataframes_list = [
    expected_performance_dataframe_multiple_days,
    expected_pdf_session_dataframe_multiple_days,
]


@pytest.mark.parametrize(
    "results_file_fixture, data_frame_method, expected_result",
    (
        (
            "get_results_single_file",
            get_performance_data_frame,
            expected_performance_dataframe,
        ),
        (
            "get_results_single_file_with_pdf_endpoint",
            get_additional_metrics_data_frame,
            expected_pdf_session_dataframe,
        ),
    ),
)
def test_get_data_frame_single_file(
    results_file_fixture, data_frame_method, expected_result, request
):
    dataframe = data_frame_method(request.getfixturevalue(results_file_fixture))
    assert_frame_equal(dataframe, expected_result)


@pytest.mark.parametrize(
    "folders, data_frame_method, expected_result",
    (
        (
            [
                "./tests/mock_stats/2024-02-07T03:09:41",
                "./tests/mock_stats/2024-02-06T03:09:41",
            ],
            get_performance_data_frame,
            expected_performance_dataframe_consecutive_days,
        ),
        (
            [
                "./tests/mock_stats/2024-02-09T03:09:41",
                "./tests/mock_stats/2024-02-12T03:09:41",
            ],
            get_additional_metrics_data_frame,
            expected_pdf_session_dataframe_consecutive_days,
        ),
    ),
)
def test_get_data_frame_multiple_files(folders, data_frame_method, expected_result):
    results = get_results(folders=folders)
    dataframe = data_frame_method(results)
    assert_frame_equal(dataframe, expected_result)


@pytest.mark.parametrize(
    "expected_dataframe, data_frame_method, results_file",
    (
        (
            expected_performance_dataframe,
            get_performance_data_frame,
            "get_results_single_file",
        ),
        (
            expected_pdf_session_dataframe,
            get_additional_metrics_data_frame,
            "get_results_single_file_with_pdf_endpoint",
        ),
    ),
)
def test_plot_data_df(
    expected_dataframe, data_frame_method, results_file, mocker, request
):
    dataframe = data_frame_method(request.getfixturevalue(results_file))

    mock_plot_data = mocker.patch("scripts.visualise_results.plot_data")
    mock_plot_data(dataframe, 1)

    assert mock_plot_data.call_count == 1
    assert_frame_equal(mock_plot_data.call_args[0][0], expected_dataframe)


@pytest.mark.parametrize(
    "results_file, data_frame_method, image_name",
    (
        (
            "get_results_single_file",
            get_performance_data_frame,
            "performance_graph.png",
        ),
        (
            "get_results_single_file_with_pdf_endpoint",
            get_additional_metrics_data_frame,
            "additional_metrics.png",
        ),
    ),
)
def test_individual_graph_creation(
    results_file, data_frame_method, image_name, mocker, request
):
    dataframe = data_frame_method(request.getfixturevalue(results_file))
    try:
        graph_creation = mocker.patch("matplotlib.pyplot.subplot")
        create_graph([dataframe], 1, image_name)
        assert graph_creation.call_count == 1
    except GraphGenerationFailed:
        pytest.fail("Graph generation failed")


@freeze_time("2024-03-1")
def test_get_dataframes():
    folders = sorted(glob(f"tests/mock_stats/*"))
    dataframes = get_dataframes(folders, 30)

    for i, item in enumerate(dataframes):
        assert_frame_equal(item, dataframes_list[i])


def test_create_graph_failed():
    dataframe = DataFrame.from_dict({})
    with pytest.raises(GraphGenerationFailed):
        create_graph([dataframe], 1, "test_graph.png")


def test_create_graph(
    mocker, get_results_single_file_with_pdf_endpoint, get_results_single_file
):
    metrics_dataframe = get_additional_metrics_data_frame(
        get_results_single_file_with_pdf_endpoint
    )
    performance_data_frame = get_performance_data_frame(get_results_single_file)
    try:
        graph_output = mocker.patch("matplotlib.pyplot.savefig")
        create_graph(
            [metrics_dataframe, performance_data_frame], 1, "additional_metrics.png"
        )
        assert graph_output.call_count == 1
    except GraphGenerationFailed:
        pytest.fail("Graph generation failed")
