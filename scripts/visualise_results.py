import sys
from glob import glob

import statistics
from pandas import DataFrame
import matplotlib.pyplot as plt


def get_stats(folders):
    results_list = []

    for folder in folders:

        get_request_response_times = []
        post_request_response_times = []
        all_response_times = []

        for file in glob(folder + '/*distribution.csv'):

            with open(file) as f:
                data = f.read()

            get_values = []
            post_values = []

            for line in data.split('\n'):
                if 'Name' in line:
                    continue

                values = line.split(',')
                percentile_99th = int(values[9])

                if 'GET /questionnaire' in line:
                    get_values.append(percentile_99th)
                if 'POST /questionnaire' in line:
                    post_values.append(percentile_99th)

            get_request_response_times.extend(get_values)
            post_request_response_times.extend(post_values)

            all_response_times = get_values + post_values

        date = folder.split('/')[-1].split('T')[0]

        results_list.append([date,
                            statistics.mean(get_request_response_times),
                            statistics.mean(post_request_response_times),
                            statistics.mean(all_response_times)])

    output_df = DataFrame(results_list, columns=["DATE", "GET", "POST", "AGGREGATE"])

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
    if len(sys.argv) != 2:
        print("Provide the benchmark outputs directory as a parameter e.g. outputs/daily-test")
    else:
        output_folder = sys.argv[-1]

        test_run_folders = sorted(glob(f"{output_folder}/*"))

        data_frame = get_stats(test_run_folders)

        plot_data(data_frame)
