#!/bin/bash

echo "Running Locust benchmark"
USER_WAIT_TIME_MIN_SECONDS=0 USER_WAIT_TIME_MAX_SECONDS=0 REQUESTS_JSON="${1}" HOST="${2:-http://localhost:5000}" pipenv run locust --no-web -c 1 -r 1 -t ${3:-1m} --csv=${4:-output} -L WARNING
