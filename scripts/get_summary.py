import os
import statistics
import sys
from datetime import datetime, timedelta
from glob import glob
from scripts.get_stats import get_stats


def get_results(folders, number_of_days=None):
    results_list = []
    from_date = (
        (datetime.utcnow() - timedelta(days=number_of_days)) if number_of_days else None
    )

    for folder in folders:
        date = folder.split("/")[-1].split("T")[0]
        if from_date and datetime.strptime(date, "%Y-%m-%d") < from_date:
            continue

        get_request_response_times = []
        post_request_response_times = []

        stats = get_stats(folder)

        get_request_response_times.extend(stats.get)
        post_request_response_times.extend(stats.post)

        all_response_times = stats.get + stats.post

        results_list.append(
            [
                date,
                statistics.mean(get_request_response_times),
                statistics.mean(post_request_response_times),
                statistics.mean(all_response_times),
                stats.total_requests,
                stats.total_failures,
                (stats.total_failures * 100) / stats.total_requests,
            ]
        )

    return results_list


def parse_environment_variables():
    output_dir = os.getenv("OUTPUT_DIR")

    if not output_dir:
        print(
            "'OUTPUT_DIR' environment variable must be provided e.g. outputs/daily-test"
        )
        sys.exit(1)

    days = os.getenv("NUMBER_OF_DAYS")
    if days and days.isdigit() is False:
        print("'NUMBER_OF_DAYS' environment variable must be a valid integer value")
        sys.exit(1)

    days = int(days) if days else None
    output_date = os.getenv("OUTPUT_DATE")

    return {
        "output_dir": output_dir,
        "number_of_days": days,
        "output_date": output_date,
    }


if __name__ == "__main__":
    parsed_variables = parse_environment_variables()
    date_to_output = parsed_variables["output_date"]

    sorted_folders = sorted(glob(f"{parsed_variables['output_dir']}/*"))
    result = get_results(sorted_folders)

    for result in result[::-1]:
        summary = (
            f"Questionnaire GETs average: {int(result[1])}ms\n"
            f"Questionnaire POSTs average: {int(result[2])}ms\n"
            f"All requests average: {int(result[3])}ms\n"
            f"Total Requests: {int(result[4])}\n"
            f"Total Failures: {int(result[5])}\n"
            f"Error Percentage: {(round(result[6], 2))}%"
        )

        if date_to_output:
            if result[0] == date_to_output:
                print(summary)
                break
        else:
            print(f"{result[0]}\n" f"{summary}\n")
