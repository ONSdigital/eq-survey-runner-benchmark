import os
import statistics
import sys
from glob import glob


def get_results(folders):

    results = {
        "get": [],
        "post": [],
        "average_get": None,
        "average_post": None,
        "average_total": None,
        "total_requests": 0,
        "total_failures": 0,
        "error_percentage": 0
    }

    for folder in folders:
        for file in glob(folder + '/*stats.csv'):

            with open(file) as f:
                data = f.read()

            for line in data.split('\n'):
                if 'Name' in line:
                    continue

                values = line.split(',')

                percentile_99th = int(values[18])
                if values[1].startswith('"/questionnaire'):
                    if values[0] == '"GET"':
                        results["get"].append(percentile_99th)
                    elif values[0] == '"POST"':
                        results["post"].append(percentile_99th)

                if 'Aggregated' in line:
                    results["total_requests"] = results["total_requests"] + int(values[2])
                    results["total_failures"] = results["total_failures"] + int(values[3])

        results["average_get"] = statistics.mean(results["get"])
        results["average_post"] = statistics.mean(results["post"])
        results["average_total"] = statistics.mean(results["get"] + results["post"])
        results["error_percentage"] = (results["total_failures"] * 100) / results["total_requests"]

    return results


def parse_environment_variables():
    output_dir = os.getenv("OUTPUT_DIR")

    if not output_dir:
        print(
            "'OUTPUT_DIR' environment variable must be provided e.g. outputs/daily-test"
        )
        sys.exit(1)

    return output_dir


if __name__ == '__main__':
    folder = parse_environment_variables()

    sorted_folders = sorted(glob(f"{folder}/*"))
    result = get_results(sorted_folders)

    summary = (
        f'Questionnaire GETs average: {int(result["average_get"])}ms\n'
        f'Questionnaire POSTs average: {int(result["average_post"])}ms\n'
        f'All requests average: {int(result["average_total"])}ms\n'
        f'Total Requests: {int(result["total_requests"])}\n'
        f'Total Failures: {int(result["total_failures"])}\n'
        f'Error Percentage: {(round(result["error_percentage"], 2))}%\n'
    )

    print(summary)