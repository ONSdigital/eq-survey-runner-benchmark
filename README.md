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

---

## Deployment with [Helm](https://helm.sh/)

To deploy this application with helm, you must have a kubernetes cluster already running and be logged into the cluster.

Log in to the cluster using:

```
gcloud container clusters get-credentials survey-runner --region <region> --project <gcp_project_id>
```

You need to have Helm installed locally

1. Install Helm with `brew install kubernetes-helm` and then run `helm init --client-only`

2. Install Helm Tiller plugin for _Tillerless_ deploys `helm plugin install https://github.com/rimusz/helm-tiller`


### Deploying the app

To deploy the app to the cluster, run the following command:

```
helm tiller run \
-    helm upgrade --install \
-    runner-benchmark \
-    k8s/helm \
-    --set host=${HOST} \
-    --set container.image=${DOCKER_REGISTRY}/eq-survey-runner-benchmark:${IMAGE_TAG}
```

## Future Improvements

- Allow rerunning a test using the original timings rather than a random wait time between GET requests.
- Customisable HAR filters to allow this project to be used for other websites.
- Standardise method to saturate server or a benchmark format.
