#!/bin/bash

echo "Running Locust benchmark"
locust -f runner_benchmark/har_replay_test.py --host=http://localhost:5000 --no-web -c 1 -r 1 --csv=output -t 1m -L WARNING
./scripts/output_processor.py
