# Using Concourse

Deploying and destroying the infrastructure is possible via Concourse tasks.

## Prerequisites

Log in (via `fly`) to a Concourse instance that has access to the target GCP project:

```sh
fly login -t <target-concourse>
```

### Benchmark
The following env vars must be set:

- PROJECT_ID
- REGION
- REQUESTS_JSON
- LOCUST_OPTIONS
- RUNNER_FULLY_QUALIFIED_DOMAIN_NAME
- DOCKER_REGISTRY
- IMAGE_TAG
- USER_WAIT_TIME_MIN_SECONDS
- USER_WAIT_TIME_MAX_SECONDS
- PARALLELISM
- TIMEOUT
- OUTPUT_DIR
- OUTPUT_BUCKET

The following env var already has a sensible default, but can be set with alternative value if needed:
- REGION: 

## Provisioning
Use the `fly execute` command to run the task.

### Output statistics to Slack task
```sh
PROJECT_ID=<project_id> \
REQUESTS_JSON=<path_to_requests_file> \
LOCUST_OPTIONS=<additional_locust_option> \
RUNNER_FULLY_QUALIFIED_DOMAIN_NAME=<runner_fqdn> \
DOCKER_REGISTRY=<docker_registry_for_app_images> \
IMAGE_TAG=<image_tag> \
USER_WAIT_TIME_MIN_SECONDS=<user_min_wait_time> \
USER_WAIT_TIME_MAX_SECONDS=<user_max_wait_time< \
PARALLELISM=<number_of_jobs_to_run> \
TIMEOUT=<job_timeout> \
OUTPUT_DIR=<folder_where_outputs_are_stored> \
fly -t census-eq execute \
  --config ci/run_benchmark.yaml
```

### Notifcation of performance statistics to Slack
The following env vars must be set:

- OUTPUT_BUCKET
- OUTPUT_DIR
- SLACK_CHANNEL_NAME

The following env var already has a sensible default, but can be set with alternative value if needed:
- SLACK_AUTH_TOKEN

## Provisioning
Use the `fly execute` command to run the task.

### Output statistics to Slack task
```sh
OUTPUT_BUCKET_NAME=<output_bucket_name> \
OUTPUT_DIR=<output_directory> \
SLACK_CHANNEL_NAME=<slack_channel_name> \
fly -t census-eq execute \
  --config ci/output-stats-to-slack.yaml
```