import json
import os
from glob import glob

import requests
import statistics
from cachetools import cached, TTLCache

test_run_folders = sorted(glob("outputs/timed-schedule/*"))
cache = TTLCache(maxsize=1000, ttl=300)


@cached(cache)
def get_runner_branch_for_commit_hash(commit_hash):
    response = requests.get(
        f'https://api.github.com/repos/ONSdigital/eq-questionnaire-runner/git/commits/{commit_hash}',
        auth=('MebinAbraham', os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')),
    )

    if response.status_code == 200:
        return response.json().get('message')


def get_stats():
    for folder in test_run_folders:

        get_request_response_times = []
        post_request_response_times = []
        all_response_times = []

        for file in os.listdir(folder):
            if 'distribution.csv' not in file:
                continue

            with open(f'{os.getcwd()}/{folder}/{file}') as f:
                data = f.read()

            get_values = []
            post_values = []

            for line in data.split('\n'):
                if 'Name' in line:
                    continue

                values = line.split(',')
                percentile_99th = int(values[9])

                if 'GET /questionnaire' in line:
                    get_values.append(percentile_99th)
                if 'POST /questionnaire' in line:
                    post_values.append(percentile_99th)
                if 'Aggregated' in line:
                    all_response_times.append(percentile_99th)

            get_request_response_times.append(int(sum(get_values) / len(get_values)))
            post_request_response_times.append(int(sum(post_values) / len(post_values)))

            with open(
                f'{os.getcwd()}/{folder}/{file}'.replace('.csv', '-metadata.json')
            ) as f:
                metadata = json.loads(f.read())

        print(
            f'Test Run: {folder} - Runner version: {get_runner_branch_for_commit_hash(metadata["runner_version"])}'
        )
        print(
            f'Questionnaire GETs average: {statistics.mean(get_request_response_times)}ms'
        )
        print(
            f'Questionnaire POSTs average: {statistics.mean(post_request_response_times)}ms'
        )
        print(f'All requests average: {statistics.mean(all_response_times)}ms\n')


if __name__ == '__main__':
    get_stats()
