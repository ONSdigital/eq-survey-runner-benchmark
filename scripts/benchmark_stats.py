from csv import DictReader
from glob import glob
from typing import List


class BenchmarkStats:
    def __init__(self, folder_paths: List[str]):
        self._files: List = []
        for folder_path in folder_paths:
            self._files.extend(glob(f"{folder_path}/*stats.csv"))

        self.weighted_get_requests: List[int] = []
        self.weighted_post_requests: List[int] = []
        self._total_requests: int = 0
        self._total_failures: int = 0
        self._total_get_requests: int = 0
        self._total_post_requests: int = 0
        self._process_file_data()

    def __str__(self):
        return (
            f'GETs average: {int(self.average_weighted_get)}ms\n'
            f'POSTs average: {int(self.average_weighted_post)}ms\n'
            f'All requests average: {int(self.average_weighted_total)}ms\n'
            f'Total Requests: {int(self._total_requests):,}\n'
            f'Total Failures: {int(self._total_failures):,}\n'
            f'Error Percentage: {(round(self.error_percentage, 2))}%\n'
        )

    def _process_file_data(self):
        for file in self.files:
            with open(file) as fp:
                for row in DictReader(fp, delimiter=","):
                    percentile_99th = int(row["99%"])
                    request_count = int(
                        row.get("Request Count") or row.get("# requests")
                    )

                    if row["Type"] == "GET":
                        self.weighted_get_requests.append(
                            percentile_99th * request_count
                        )
                        self._total_get_requests += request_count
                    elif row["Type"] == "POST":
                        self.weighted_post_requests.append(
                            percentile_99th * request_count
                        )
                        self._total_post_requests += request_count
                    elif row["Name"] == "Aggregated":
                        failure_count = row.get("Failure Count") or row.get(
                            "# failures"
                        )
                        self._total_failures += int(failure_count)
                        self._total_requests += request_count

    @property
    def files(self) -> List[str]:
        return self._files

    @property
    def average_weighted_get(self):
        return sum(self.weighted_get_requests) / self._total_get_requests

    @property
    def average_weighted_post(self):
        return sum(self.weighted_post_requests) / self._total_post_requests

    @property
    def average_weighted_total(self):
        return (
            sum(self.weighted_get_requests + self.weighted_post_requests)
            / self._total_requests
        )

    @property
    def error_percentage(self):
        return (self._total_failures * 100) / self._total_requests
