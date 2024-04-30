import os
import sys
from datetime import datetime, timedelta
from glob import glob
from typing import NamedTuple

from scripts.benchmark_stats import BenchmarkStats


class Result(NamedTuple):
    date: str
    statistics: BenchmarkStats
    output_to_github: bool = False

    def __str__(self):
        if self.output_to_github:
            return f'{self.date}\n{{"body": "{{{self.statistics}\n"}}'
        return f"{self.date}\n{self.statistics}\n"


def get_results(folders, output_to_github=False, number_of_days=None):
    from_date = (
        (datetime.utcnow() - timedelta(days=number_of_days)) if number_of_days else None
    )

    for folder in folders:
        date = folder.split("/")[-1].split("T")[0]
        if from_date and datetime.strptime(date, "%Y-%m-%d") < from_date:
            continue
        yield Result(date, BenchmarkStats([folder], output_to_github), output_to_github)


def parse_environment_variables():
    days = os.getenv("NUMBER_OF_DAYS")
    if days and days.isdigit() is False:
        print("'NUMBER_OF_DAYS' environment variable must be a valid integer value")
        sys.exit(1)

    days = int(days) if days else None

    return {
        "number_of_days": days,
        "output_date": os.getenv("OUTPUT_DATE"),
        "output_dir": os.getenv("OUTPUT_DIR", "outputs"),
        "output_to_github": os.getenv("OUTPUT_TO_GITHUB"),
    }


if __name__ == "__main__":
    parsed_variables = parse_environment_variables()
    date_to_output = parsed_variables["output_date"]
    output_to_github = bool(parsed_variables["output_to_github"])
    sorted_folders = sorted(glob(f"{parsed_variables['output_dir']}/*"), reverse=True)
    results = get_results(sorted_folders, output_to_github)

    for result in results:
        if date_to_output:
            if result.date == date_to_output:
                print(result.statistics)
                break
        else:
            print(result)
