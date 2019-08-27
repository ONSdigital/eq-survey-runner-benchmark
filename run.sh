#!/bin/bash

echo "Running Locust benchmark"
REQUESTS_JSON="${1}" HOST="${2:-http://localhost:5000}" pipenv run locust --no-web -c 1 -r 1 -t 1m --csv=output -L WARNING
./scripts/output_processor.py
