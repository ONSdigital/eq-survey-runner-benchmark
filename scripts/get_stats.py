from dataclasses import dataclass, field
from glob import glob

@dataclass
class BenchmarkStats:
    get: [int] = field(default_factory=list)
    post: [int] = field(default_factory=list)
    average_get: int = None
    average_post: int = None
    average_total: int = None
    total_requests: int = 0
    total_failures: int = 0
    error_percentage: int = 0


def get_stats(folder):
    stats = BenchmarkStats()

    for file in glob(folder + "/*stats.csv"):

        with open(file) as f:
            data = f.read()

        for line in data.split("\n"):
            if "Name" in line:
                continue

            values = line.split(",")

            percentile_99th = int(values[18])
            if values[1].startswith('"/questionnaire'):
                if values[0] == '"GET"':
                    stats.get.append(percentile_99th)
                elif values[0] == '"POST"':
                    stats.post.append(percentile_99th)

        if "Aggregated" in line:
            stats.total_requests = stats.total_requests + int(values[2])
            stats.total_failures = stats.total_failures + int(values[3])

    return stats
