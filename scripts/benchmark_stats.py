import os
from collections import defaultdict
from csv import DictReader
from glob import glob
from typing import List, Mapping


class BenchmarkStats:
    PERCENTILES_TO_REPORT = (50, 90, 95, 99, 99.9)
    PERCENTILE_TO_USE_FOR_AVERAGES = 99

    def __init__(self, folder_paths: List[str]):
        self._files: List = []
        self.output_to_github = os.getenv("OUTPUT_TO_GITHUB", False)
        for folder_path in folder_paths:
            self._files.extend(glob(f"{folder_path}/*stats.csv"))

        self._requests: Mapping = {
            "GET": {"response_times": [], "total": 0},
            "POST": {"response_times": [], "total": 0},
        }

        self._session_percentile: List[int] = []
        self._pdf_percentile: List[int] = []
        self._total_failures: int = 0
        self._percentiles: Mapping[int : List[float]] = defaultdict(list)  # noqa: E203

        self._process_file_data()

    def __str__(self):
        formatted_percentiles = "\n".join(
            f"{percentile}th: {self.percentiles[percentile]}ms"
            for percentile in self.PERCENTILES_TO_REPORT
        )
        formatted_metrics = {
            "average_get": self.formatted_percentile(self.average_get),
            "average_post": self.formatted_percentile(self.average_post),
            "pdf_percentile": self.formatted_percentile(self.pdf_percentile),
            "session_percentile": self.formatted_percentile(self.session_percentile),
        }
        if self.output_to_github:
            formatted_percentiles = formatted_percentiles.replace(os.linesep, "<br />")
            return (
                f'{{"body": "'
                f"**Benchmark Results**<br /><br />"
                f"Percentile Averages:<br />"
                f"{formatted_percentiles}<br />"
                f"GETs (99th): {formatted_metrics['average_get']}<br />"
                f"POSTs (99th): {formatted_metrics['average_post']}<br /><br />"
                f"PDF: {formatted_metrics['pdf_percentile']}<br />"
                f"Session: {formatted_metrics['session_percentile']}<br /><br />"
                f"Total Requests: {self.total_requests:,}<br />"
                f"Total Failures: {self._total_failures:,}<br />"
                f'Error Percentage: {(round(self.error_percentage, 2))}%<br />"}}'
            )
        return (
            f"---\n"
            f"Percentile Averages:\n"
            f"{formatted_percentiles}\n"
            f"---\n"
            f"GETs (99th): {formatted_metrics['average_get']}\n"
            f"POSTs (99th): {formatted_metrics['average_post']}\n"
            f"---\n"
            f"PDF: {formatted_metrics['pdf_percentile']}\n"
            f"Session: {formatted_metrics['session_percentile']}\n"
            f"---\n"
            f"Total Requests: {self.total_requests:,}\n"
            f"Total Failures: {self._total_failures:,}\n"
            f"Error Percentage: {(round(self.error_percentage, 2))}%\n"
        )

    def _process_file_data(self):
        for file in self.files:
            with open(file) as fp:
                for row in DictReader(fp, delimiter=","):
                    request_count = int(
                        row.get("Request Count") or row.get("# requests")
                    )
                    if row["Name"] == "Aggregated":
                        failure_count = row.get("Failure Count") or row.get(
                            "# failures"
                        )
                        self._total_failures += int(failure_count)
                    else:
                        if row["Name"] == "/submitted/download-pdf":
                            self._pdf_percentile.append(round(float(row.get("99%"))))

                        if row["Name"] == "/session":
                            self._session_percentile.append(
                                round(float(row.get("99%")))
                            )

                        weighted_request_count = self._get_weighted_request_count(
                            request_count
                        )
                        for percentile in self.PERCENTILES_TO_REPORT:
                            weighted_percentile = (
                                float(row[f"{percentile}%"]) * weighted_request_count
                            )
                            self._percentiles[percentile].append(weighted_percentile)

                        percentile_response_time = float(
                            row[f"{self.PERCENTILE_TO_USE_FOR_AVERAGES}%"]
                        )
                        weighted_response_time = (
                            percentile_response_time * weighted_request_count
                        )
                        self._requests[row["Type"]]["response_times"].append(
                            weighted_response_time
                        )
                        self._requests[row["Type"]]["total"] += request_count

    @property
    def pdf_percentile(self) -> int | None:
        if self._pdf_percentile:
            average_pdf_percentile = float(
                sum(self._pdf_percentile) / len(self._pdf_percentile)
            )
            return round(average_pdf_percentile)
        return None

    @property
    def session_percentile(self) -> int:
        return round(sum(self._session_percentile) / len(self._session_percentile))

    @property
    def files(self) -> List[str]:
        return self._files

    @property
    def percentiles(self) -> Mapping:
        return {
            percentile: round(
                float(
                    sum(values) / self._get_weighted_request_count(self.total_requests)
                )
            )
            for percentile, values in self._percentiles.items()
        }

    @property
    def total_requests(self) -> int:
        return self._requests["GET"]["total"] + self._requests["POST"]["total"]

    @property
    def average_get(self) -> int:
        return round(
            float(
                sum(self._requests["GET"]["response_times"])
                / self._get_weighted_request_count(self._requests["GET"]["total"])
            )
        )

    @property
    def average_post(self) -> int:
        return round(
            float(
                sum(self._requests["POST"]["response_times"])
                / self._get_weighted_request_count(self._requests["POST"]["total"])
            )
        )

    @property
    def error_percentage(self) -> float:
        return (self._total_failures * 100) / self.total_requests

    @staticmethod
    def formatted_percentile(percentile) -> str:
        if percentile:
            return f"{percentile}ms"
        return "N/A"

    def _get_weighted_request_count(self, request_count: int) -> float:
        return request_count * self.PERCENTILE_TO_USE_FOR_AVERAGES / 100
