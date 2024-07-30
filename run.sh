#!/bin/bash

echo "Running Locust benchmark"
USER_WAIT_TIME_MIN_SECONDS=0 USER_WAIT_TIME_MAX_SECONDS=0 REQUESTS_JSON="${1}" INCLUDE_SCHEMA_URL_IN_TOKEN="${2}" HOST="${3:-http://localhost:5000}"  poetry run locust --headless -u 1 -r 1 -t ${4:-1m} --csv=${5:-output} -L WARNING
