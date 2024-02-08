from glob import glob

import matplotlib.pyplot as plt
from pandas import DataFrame

from scripts.get_summary import get_results, parse_environment_variables

PERCENTILES_TO_GRAPH = (50, 90, 95, 99)


class GraphGenerationFailed(Exception):
    pass


def plot_data(df, number_of_days_to_plot):
    try:
        plt.style.use('fast')

        if (
            number_of_days_to_plot and number_of_days_to_plot <= 45
        ):  # To make the chart still easily digestible
            df.plot.line(marker="o", markersize=8)
            # plt.grid(True, axis="both", alpha=0.3)
        else:
            df.plot.line()

        plt.margins(0.03, 0.07)
        plt.legend(frameon=True, prop={"size": 17})
        plt.xticks(df.index, df["DATE"], size="small", rotation=90)
        plt.yticks(size="small")
        plt.ylabel("Average Response Time (ms)")
        plt.xlabel("Run Date (YYYY-MM-DD)", labelpad=13)

        plt.savefig('performance_graph.png', bbox_inches="tight")
        print("Graph saved as performance_graph.png")
    except Exception as e:
        raise GraphGenerationFailed from e


def get_data_frame(results):
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

    percentile_columns = (f"{percentile}th" for percentile in PERCENTILES_TO_GRAPH)
    return DataFrame(result_fields, columns=["DATE", *percentile_columns])


if __name__ == '__main__':
    parsed_variables = parse_environment_variables()
    number_of_days = parsed_variables['number_of_days']

    folders = sorted(glob(f"{parsed_variables['output_dir']}/*"))
    results = get_results(folders, number_of_days)
    dataframe = get_data_frame(results)

    plot_data(dataframe, number_of_days)
