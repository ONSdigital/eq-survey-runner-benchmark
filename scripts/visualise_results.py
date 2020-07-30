from glob import glob

import matplotlib.pyplot as plt
from pandas import DataFrame

from scripts.get_summary import get_results, parse_environment_variables


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
    parsed_variables = parse_environment_variables()

    folders = sorted(glob(f"{parsed_variables['output_dir']}/*"))
    results = get_results(folders, parsed_variables['number_of_days'])
    result_fields = [
        [
            result[0],
            result[1].average_get,
            result[1].average_post,
            result[1].average_total,
        ]
        for result in results
    ]

    data_frame = DataFrame(result_fields, columns=["DATE", "GET", "POST", "AVERAGE"])

    plot_data(data_frame)
