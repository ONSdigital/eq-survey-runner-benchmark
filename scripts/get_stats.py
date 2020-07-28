from dataclasses import dataclass
from glob import glob

@dataclass
class BenchmarkStats:
    get: []
    post: []
    average_get: None
    average_post: None
    average_total: None
    total_requests: int
    total_failures: int
    error_percentage: int

    def __init__(self):
        self.get = []
        self.post = []
        self.average_get = None
        self.average_post = None
        self.total_requests = 0
        self.total_failures = 0
        self.error_percentage = 0


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
