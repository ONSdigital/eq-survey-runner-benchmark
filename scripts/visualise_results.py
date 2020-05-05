import os
import sys
from glob import glob

import matplotlib.pyplot as plt
from pandas import DataFrame

from scripts.get_summary import get_stats


def create_data_frame(results_list):
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
    output_folder = os.getenv("OUTPUT_DIR")

    if not output_folder:
        print("'OUTPUT_DIR' environment variable must be provided e.g. outputs/daily-test")
        sys.exit(1)

    filter_after = os.getenv("FILTER_AFTER")
    folders = sorted(glob(f"{output_folder}/*"))

    results = get_stats(folders, filter_after)
    data_frame = create_data_frame(results)

    plot_data(data_frame)
