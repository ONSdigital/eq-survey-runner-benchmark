# EQ Performance Benchmark

This is a performance benchmarking tool designed to measure the performance of [EQ Survey Runner](https://github.com/ONSDigital/eq-survey-runner) using [locust](https://locust.io/).

This repository was heavily inspired by the [census performance tests](https://github.com/ONSdigital/census-eq-performance-tests).

## Running a benchmark

The benchmark consumes a requests JSON file that contains a list of HTTP requests. This can either be created from scratch or generated from a HAR file. Example requests files can be found in the `requests` folder.

To run a benchmark, use:

```bash
pipenv run ./run.sh <REQUESTS_JSON> <HOST: Optional>
```
e.g.
```bash
pipenv run ./run.sh requests/test_checkbox.json
```

This will run 1 minute of locust requests with 1 user and no wait time between requests. The output file can be found in `output_requests_processed.csv`.

For the web interface:

```bash
REQUESTS_JSON=requests/test_checkbox.json HOST=http://localhost:5000 pipenv run locust
```

## Configuration

The following environment variables can be used to configure the locust test:

- `REQUESTS_JSON` - The filepath of the requests file relative to the base project directory
  - Defaults to `requests.json`
- `HOST` - The host name the benchmark is run against.
- `USER_WAIT_TIME_MIN_SECONDS` - The minimum delay between each user's GET requests
  - defaults to zero
- `USER_WAIT_TIME_MAX_SECONDS` - The maximum delay between each user's GET requests
  - defaults to zero

## Generating a requests file

Open the network inspector in Chrome or Firefox and ensure 'preserve log' is ticked. Run your manual or functional test. 

**Important:** The captured test should not include the `/session` endpoint.

After the test is complete, right-click on one of the requests in the network inspector and save the log as a HAR file. To generate a requests file from the HAR file run:

```bash
pipenv run python generate_requests.py <HAR_FILEPATH> <REQUESTS_FILEPATH> <SCHEMA_NAME>
```
e.g.
```bash
pipenv run python generate_requests.py requests.har requests/test_checkbox.json test_checkbox
```

## Using Docker to run the tests

To run the load test in a docker container, firstly build the image 

```
build -t <YOUR_CONTAINER_NAME> .
```
Then run the docker image with the commands below, variables additional to the ones mentioned above in configuration are

- `SWARM_SIZE` (optional) The amount of users you want to test with.
- `HATCH_RATE` (optional) The speed at which user are introduced.
- `DURATION` (optional) The length of the test, m for minutes, h for hours.

All variables above will default to 1 if not set
```
docker run --env REQUESTS_JSON=<REQUEST_JSON> --env HOST=<HOST>  --env USER_WAIT_TIME_MIN_SECONDS=<USER_WAIT_TIME_MIN_SECONDS> --env USER_WAIT_TIME_MAX_SECONDS=<USER_WAIT_TIME_MAX_SECONDS --env SWARM_SIZE=<SWARM_SIZE> --env HATCH_RATE=<HATCH_RATE> --env DURATION=<DURATION>  <CONTAINER_NAME>
```

e.g.
```
docker run --env REQUESTS_JSON=requests/census_individual_gb_eng.json --env HOST=http://localhost:5000  --env USER_WAIT_TIME_MIN_SECONDS=5 --env USER_WAIT_TIME_MAX_SECONDS=15 --env SWARM_SIZE=250 --env HATCH_RATE=250 --env DURATION=1m  my_container
```

N.B As the wait is only on the GET, and requests invariable come in pairs e.g. POST then GET, you will effectively get 2 requests for your average wait time. Looking at the example above you might expect to generate load of 25 RPS (250 users answering on average every 10 seconds), however you will get 50 RPS for the reason mentioned.

## Future Improvements

- Allow rerunning a test using the original timings rather than a random wait time between GET requests.
- Customisable HAR filters to allow this project to be used for other websites.
- Standardise method to saturate server or a benchmark format.
