from datetime import datetime, timedelta
from glob import glob
import os
import sys
from typing import List, NamedTuple

from scripts.benchmark_stats import BenchmarkStats


class Result(NamedTuple):
    date: str
    statistics: List[str]

    def __str__(self):
        return f"{self.date}\n{self.statistics}\n"


def get_results(folders, number_of_days=None):
    from_date = (
        (datetime.utcnow() - timedelta(days=number_of_days)) if number_of_days else None
    )

    for folder in folders:
        date = folder.split("/")[-1].split("T")[0]
        if from_date and datetime.strptime(date, "%Y-%m-%d") < from_date:
            continue
        yield Result(date, BenchmarkStats(folder))


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
    results = get_results(sorted_folders)

    for result in results:
        if date_to_output:
            if result.date == date_to_output:
                print(result.statistics)
                break
        else:
            print(result)
