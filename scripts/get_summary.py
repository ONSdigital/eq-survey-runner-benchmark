import os
import statistics
import sys
from glob import glob


def get_stats(folders, filter_after=None):
    results_list = []

    for folder in folders:
        date = folder.split('/')[-1].split('T')[0]
        if filter_after and date <= filter_after:
            continue

        get_request_response_times = []
        post_request_response_times = []
        all_response_times = []

        for file in glob(folder + '/*stats.csv'):

            with open(file) as f:
                data = f.read()

            get_values = []
            post_values = []

            for line in data.split('\n'):
                if 'Name' in line:
                    continue

                values = line.split(',')

                percentile_99th = int(values[18])
                if values[1].startswith('"/questionnaire'):
                    if values[0] == '"GET"':
                        get_values.append(percentile_99th)
                    elif values[0] == '"POST"':
                        post_values.append(percentile_99th)

            get_request_response_times.extend(get_values)
            post_request_response_times.extend(post_values)

            all_response_times = get_values + post_values

        results_list.append(
            [
                date,
                statistics.mean(get_request_response_times),
                statistics.mean(post_request_response_times),
                statistics.mean(all_response_times),
            ]
        )

    return results_list


if __name__ == '__main__':
    output_folder = os.getenv("OUTPUT_DIR")

    if not output_folder:
        print(
            "'OUTPUT_DIR' environment variable must be provided e.g. outputs/daily-test"
        )
        sys.exit(1)

    run_date = os.getenv("RUN_DATE")
    folders = sorted(glob(f"{output_folder}/*"))
    stats = get_stats(folders)

    for stat in stats:
        summary = (
            f'Questionnaire GETs average: {int(stat[1])}ms\n'
            f'Questionnaire POSTs average: {int(stat[2])}ms\n'
            f'All requests average: {int(stat[3])}ms'
        )

        if run_date:
            if stat[0] == run_date:
                print(summary)
                break
        else:
            print(summary)
