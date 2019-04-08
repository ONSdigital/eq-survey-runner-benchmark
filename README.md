# EQ Performance Benchmark

## Summary

This is a performance benchmarking tool designed to measure the performance of [EQ Survey Runner](https://github.com/ONSDigital/eq-survey-runner).

This repository was heavily inspired by the [census performance tests](https://github.com/ONSdigital/census-eq-performance-tests)

The benchmark uses locust to perform a load test. The locust test consists of a set of endpoints which are generated dynamically from a HAR file. This allows us run a functional test, or a manual test representing a normal user's behaviour. The HTTP requests from this test can be exported to a HAR file, which can then be imported into this benchmarking tool. The same requests will be modified slightly and rerun during the locust benchmark.

## Instructions

Open the network inspector in Chrome or Firefox and ensure 'preserve log' is ticked. Run your manual or functional test.

After the test is complete, right-click on one of the requests in the network inspector and save the log as a HAR file. Save this file in the root directory of this project as `requests.har` or alternatively use the path to this HAR file in the `HAR_FILEPATH` environment variable when running locust.

To run a benchmark, use:

```bash
pipenv install
pipenv run ./run.sh <EQ_ID> <FORM_TYPE>
```
e.g.
```
pipenv run ./run.sh test mutually_exclusive
```

This will run 1 minute of locust requests with 1 user and no wait time between requests.

The output file can be found in `output_requests_processed.csv`

If you'd like to run locust on its own, you can use the following commands

For the web interface:

```bash
EQ_ID=test FORM_TYPE=mutually_exclusive pipenv run locust -f runner_benchmark/har_replay_test.py --host=http://localhost:5000
```

For a command line interface ( with output CSV file ):

```bash
EQ_ID=test FORM_TYPE=mutually_exclusive pipenv run locust -f runner_benchmark/har_replay_test.py --host=http://localhost:5000 --no-web -t 1m -c 100 -r 10 --csv=output
```

## Configuration

The following environment variables can be used to configure the locust test:

- `HAR_FILEPATH` - The filepath of the HAR file relative to the base project directory
  - Defaults to `requests.har`
- `EQ_ID` - The eq_id of the schema being tested.
- `FORM_TYPE` - The form_type of the schema being tested.
- `USER_WAIT_TIME_MIN_SECONDS` - The minimum delay between each user's GET requests
  - defaults to zero
- `USER_WAIT_TIME_MAX_SECONDS` - The maximum delay between each user's GET requests
  - defaults to zero

## Future Improvements

- Allow rerunning a HAR file using the original timings rather than a random wait time between GET requests.
- Allow running multiple HAR files as different scenarios.
- Customisable HAR filters to allow this project to be used for other websites.
- Standardise method to saturate server or a benchmark format.
