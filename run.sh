#!/bin/bash

echo "Running Locust benchmark"
SCHEMA_NAME="${1}" HOST="${2:-http://localhost:5000}" pipenv run locust -f runner_benchmark/har_replay_test.py --no-web -t 1m -c 100 -r 10 --csv=output --no-web -c 1 -r 1 --csv=output -t 1m -L WARNING
./scripts/output_processor.py
