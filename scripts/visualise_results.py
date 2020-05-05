import sys
from glob import glob

import matplotlib.pyplot as plt
from pandas import DataFrame

from scripts.get_summary import get_stats


def create_data_frame(folders, filter_after):
    results_list = get_stats(folders, filter_after)

    output_df = DataFrame(results_list, columns=["DATE", "GET", "POST", "AVERAGE"])

    return output_df


def plot_data(df):
    plt.style.use('seaborn-poster')
    df.plot.line()
    plt.xticks(df.index, df["DATE"], size="small", rotation=90)
    plt.yticks(size="small")
    plt.ylabel("Average Response Time (ms)")
    plt.xlabel("Run Date (DD-MM)")
    plt.savefig('performance_graph.png')
    print("Graph saved as performance_graph.png")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(
            "Provide the benchmark outputs directory and optionally a date to filter after by as a parameter e.g. outputs/daily-test 2020-01-01"
        )
    else:
        output_folder = sys.argv[1]
        filter_after_date = sys.argv[2] if len(sys.argv) > 2 else None

        test_run_folders = sorted(glob(f"{output_folder}/*"))

        results_list = get_stats(folders, filter_after)
        data_frame = create_data_frame(results_list)

        plot_data(data_frame)
