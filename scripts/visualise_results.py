from glob import glob

import matplotlib.pyplot as plt
from pandas import DataFrame

from scripts.get_summary import get_results, parse_environment_variables

PERCENTILES_TO_GRAPH = (50, 90, 95, 99)
PERCENTILES_TO_PLOT = ("50th", "90th", "95th", "99th")

ADDITIONAL_METRICS_TO_GRAPH = ("PDF", "Session")


class GraphGenerationFailed(Exception):
    pass


def plot_data(dataframes, number_of_days_to_plot):
    plt.style.use("fast")
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

    for i, dataframe in enumerate(dataframes):
        """
        We use the .subplot() method below to switch the indexes of the plots themselves,
        if we do not switch plots or remove this method, the visuals (such as the graph background)
        and, most importantly, the axes values will only be applied to the second subplot.
        """
        plt.subplot(1, 2, i + 1)
        if (
            number_of_days_to_plot and number_of_days_to_plot <= 45
        ):  # To make the chart still easily digestible
            dataframe.plot.line(marker="o", markersize=8, ax=axes[i])
            plt.grid(True, axis="both", alpha=0.3)
        else:
            dataframe.plot.line(ax=axes[i])

        plt.margins(0.03, 0.07)
        plt.legend(frameon=True, prop={"size": 10})
        plt.xticks(
            dataframe.index, dataframe["DATE"], size="small", rotation=90
        )
        plt.yticks(size="small")
        plt.ylabel("Average Response Time (ms)")
        plt.xlabel("Run Date (YYYY-MM-DD)", labelpad=13)


def create_graph(dataframes, number_of_days_to_plot, filename):
    try:
        plot_data(dataframes, number_of_days_to_plot)
        plt.savefig(filename, bbox_inches="tight")
        print("Graph saved as", filename)
    except Exception as e:
        raise GraphGenerationFailed from e


def create_dataframe(result_fields, values_to_plot):
    return DataFrame(
        result_fields,
        columns=["DATE", *(f"{percentile}" for percentile in values_to_plot)],
    )


def get_performance_data_frame(results):
    result_fields = [
        [
            result.date,
            *(
                result.statistics.percentiles[percentile]
                for percentile in PERCENTILES_TO_GRAPH
            ),
        ]
        for result in results
    ]

    return create_dataframe(result_fields, PERCENTILES_TO_PLOT)


def get_additional_metrics_data_frame(results):
    result_fields = [
        [
            result.date,
            result.statistics.average_pdf_percentile,
            result.statistics.average_session_percentile,
        ]
        for result in results
    ]

    return create_dataframe(result_fields, ADDITIONAL_METRICS_TO_GRAPH)


if __name__ == "__main__":
    parsed_variables = parse_environment_variables()
    number_of_days = parsed_variables["number_of_days"]

    folders = sorted(glob(f"{parsed_variables['output_dir']}/*"))

    results = list(get_results(folders, number_of_days))

    performance_dataframe = get_performance_data_frame(results)
    additional_metrics_dataframe = get_additional_metrics_data_frame(results)

    dataframe_values = [performance_dataframe, additional_metrics_dataframe]

    create_graph(dataframe_values, number_of_days, "performance_graph.png")
