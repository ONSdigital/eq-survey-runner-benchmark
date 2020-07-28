import os
import statistics
from glob import glob
from scripts.get_stats import get_stats


def get_results(folders):
    results = {
        "get": [],
        "post": [],
        "average_get": [],
        "average_post": [],
        "average_total": [],
        "error_percentage": 0,
        "total_requests": 0,
        "total_failures": 0
    }

    for folder in folders:
        stats = get_stats(folder)
        results["get"].extend(stats["get"])
        results["post"].extend(stats["post"])
        results["total_requests"] = results["total_requests"] + stats["total_requests"]
        results["total_failures"] = results["total_failures"] + stats["total_failures"]

    results["average_get"] = statistics.mean(results["get"])
    results["average_post"] = statistics.mean(results["post"])
    results["average_total"] = statistics.mean(results["get"] + results["post"])
    results["error_percentage"] = (results["total_failures"] * 100) / results["total_requests"]

    return results


def parse_environment_variables():
    try:
        output_dir = os.environ["OUTPUT_DIR"]
    except KeyError:
        print(
            "'OUTPUT_DIR' environment variable must be set e.g. outputs/daily-test"
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