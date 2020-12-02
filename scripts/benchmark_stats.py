from collections import defaultdict
from csv import DictReader
from glob import glob
from typing import List, Mapping


class BenchmarkStats:
    PERCENTILES_TO_REPORT = (50, 90, 95, 99, 99.9, 100)
    PERCENTILES_TO_GRAPH = (50, 90, 95, 99)
    PERCENTILE_TO_USE_FOR_ROUTES = 99

    def __init__(self, folder_paths: List[str]):
        self._files: List = []
        for folder_path in folder_paths:
            self._files.extend(glob(f"{folder_path}/*stats.csv"))

        self._weighted_get_requests: List[int] = []
        self._weighted_post_requests: List[int] = []
        self._total_get_requests: int = 0
        self._total_post_requests: int = 0

        self._process_file_data()

    def __str__(self):
        formatted_percentiles = "\n".join(
            f"{percentile}th: {self._percentiles[percentile]}ms"
            for percentile in self.PERCENTILES_TO_REPORT
        )
        return (
            f'---\n'
            f'Percentiles:\n'
            f'{formatted_percentiles}\n'
            f'---\n'
            f'GETs average: {self.average_weighted_get}ms\n'
            f'POSTs average: {self.average_weighted_post}ms\n'
            f'All requests average: {self.average_weighted_total}ms\n'
            f'---\n'
            f'Total Requests: {self._total_requests:,}\n'
            f'Total Failures: {self._total_failures:,}\n'
            f'Error Percentage: {(round(self.error_percentage, 2))}%\n'
        )

    def _process_file_data(self):
        for file in self.files:
            with open(file) as fp:
                for row in DictReader(fp, delimiter=","):
                    percentile = int(row[f"{self.PERCENTILE_TO_USE_FOR_ROUTES}%"])
                    request_count = int(
                        row.get("Request Count") or row.get("# requests")
                    )
                    weighted_request = percentile * request_count

                    if row["Type"] == "GET":
                        self._weighted_get_requests.append(weighted_request)
                        self._total_get_requests += request_count
                    elif row["Type"] == "POST":
                        self._weighted_post_requests.append(weighted_request)
                        self._total_post_requests += request_count
                    elif row["Name"] == "Aggregated":
                        failure_count = row.get("Failure Count") or row.get(
                            "# failures"
                        )
                        self._total_failures = int(failure_count)
                        self._total_requests = request_count

                        self._percentiles = defaultdict(int)
                        for percentile in self.PERCENTILES_TO_REPORT:
                            self._percentiles[percentile] = int(row[f"{percentile}%"])

    @property
    def files(self) -> List[str]:
        return self._files

    @property
    def percentiles(self) -> Mapping:
        return self._percentiles

    @property
    def average_weighted_get(self) -> int:
        return sum(self._weighted_get_requests) // self._total_get_requests

    @property
    def average_weighted_post(self) -> int:
        return sum(self._weighted_post_requests) // self._total_post_requests

    @property
    def average_weighted_total(self) -> int:
        return (
            sum(self._weighted_get_requests + self._weighted_post_requests)
            // self._total_requests
        )

    @property
    def error_percentage(self) -> int:
        return (self._total_failures * 100) // self._total_requests
