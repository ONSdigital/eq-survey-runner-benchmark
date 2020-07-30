import os, sys
import statistics
from glob import glob
from scripts.get_stats import get_stats, BenchmarkStats


def get_results(folders):
    results = BenchmarkStats()

    for folder in folders:
        stats = get_stats(folder)
        results.get.extend(stats.get)
        results.post.extend(stats.post)
        results.total_requests += stats.total_requests
        results.total_failures += stats.total_failures

    results.average_get = statistics.mean(results.get)
    results.average_post = statistics.mean(results.post)
    results.average_total = statistics.mean(results.get + results.post)
    results.error_percentage = (results.total_failures * 100) / results.total_requests

    return results


if __name__ == "__main__":
    folder = os.getenv("OUTPUT_DIR")

    if not folder:
        print(
            "'OUTPUT_DIR' environment variable must be provided e.g. outputs/daily-test"
        )
        sys.exit(1)

    sorted_folders = sorted(glob(f"{folder}/*"))
    result = get_results(sorted_folders)

    print(result)
