import os, sys
import statistics
from glob import glob
from scripts import BenchmarkStats
from typing import List


def get_results(folders: List[str]) -> List:
    return [BenchmarkStats(folder) for folder in folders]


if __name__ == "__main__":
    folders_path = os.getenv("OUTPUT_DIR")

    if not folders_path:
        print(
            "'OUTPUT_DIR' environment variable must be provided e.g. outputs/daily-test"
        )
        sys.exit(1)

    sorted_folders = sorted(glob(f"{folders_path}/*"))
    results = get_results(sorted_folders)

    for result in results:
        print(result)
