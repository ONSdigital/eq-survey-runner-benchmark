#!/bin/bash

echo "Running Locust benchmark"
REQUESTS_JSON="${REQUESTS_JSON}" HOST="${HOST:-http://localhost:5000}" USER_WAIT_TIME_MIN_SECONDS="${USER_WAIT_TIME_MIN_SECONDS:-0}" USER_WAIT_TIME_MAX_SECONDS="${USER_WAIT_TIME_MAX_SECONDS:-0}" pipenv run locust --no-web -c ${SWARM_SIZE:-1} -r ${HATCH_RATE:-1} -t ${DURATION:-1m} --csv=output -L WARNING
./scripts/output_processor.py
