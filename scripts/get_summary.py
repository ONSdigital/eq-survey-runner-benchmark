import os
import statistics
import sys
from datetime import datetime, timedelta
from glob import glob


def get_results(folders, number_of_days=None):
    results_list = []
    date_valid_from = (
        (datetime.utcnow() - timedelta(days=number_of_days)) if number_of_days else None
    )

    for folder in folders:
        date = folder.split('/')[-1].split('T')[0]
        if date_valid_from and datetime.strptime(date, "%Y-%m-%d") < date_valid_from:
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


def validated_environment_variables():
    output_dir = os.getenv("OUTPUT_DIR")

    if not output_dir:
        print(
            "'OUTPUT_DIR' environment variable must be provided e.g. outputs/daily-test"
        )
        sys.exit(1)

    days = os.getenv("NUMBER_OF_DAYS")
    if days and days.isdigit() is False:
        print("'NUMBER_OF_DAYS' environment variable must be a valid integer value")
        sys.exit(2)

    days = int(days) if days else None
    return output_dir, days


if __name__ == '__main__':
    output_folder, num_days = validated_environment_variables()
    output_date = os.getenv("OUTPUT_DATE")
    sorted_folders = sorted(glob(f"{output_folder}/*"))
    result = get_results(sorted_folders, num_days)

    for result in result[::-1]:
        summary = (
            f'Questionnaire GETs average: {int(result[1])}ms\n'
            f'Questionnaire POSTs average: {int(result[2])}ms\n'
            f'All requests average: {int(result[3])}ms'
        )

        if output_date:
            if result[0] == output_date:
                print(summary)
                break
        else:
            print(f'{result[0]}\n' f'{summary}\n')
