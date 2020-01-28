import os
from glob import glob
from datetime import datetime

import statistics
import json
import pandas as pd
import matplotlib.pyplot as plt


def get_stats(folders):
    results_list = []

    for folder in folders:

        get_request_response_times = []
        post_request_response_times = []

        for file in os.listdir(folder):
            if 'distribution.csv' not in file:
                continue

            with open(f'{os.getcwd()}/{folder}/{file}') as f:
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

        results_list.append([get_run_date(folder),
                            statistics.mean(get_request_response_times),
                            statistics.mean(post_request_response_times),
                            statistics.mean(all_response_times)])

    output_df = pd.DataFrame(results_list, columns=["DATE", "GET", "POST", "AGGREGATE"])

    return output_df


def plot_data(df):
    plt.style.use('seaborn-darkgrid')
    df.plot.line()
    plt.xticks(df.index, df["DATE"])
    plt.ylabel("Average Response Time (ms)")
    plt.xlabel("Run Date (DD-MM)")
    plt.show()


def get_run_date(folder):
    for file in os.listdir(folder):
        if "output_requests-metadata.json" in file:
            with open(f'{folder}/{file}') as json_file:
                metadata = json.load(json_file)
                return datetime.utcfromtimestamp(int(metadata["timestamp"])).strftime('%d-%m')


if __name__ == '__main__':
    test_run_folders = sorted(glob("outputs/daily-test/*"))

    data_frame = get_stats(test_run_folders)

    plot_data(data_frame)
