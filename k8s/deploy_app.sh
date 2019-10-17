#!/usr/bin/env bash

set -e

if [[ -z "$HOST" ]]; then
  echo "HOST is mandatory"
  exit 1
fi

DOCKER_REGISTRY="${DOCKER_REGISTRY:-eu.gcr.io/census-eq-ci}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REQUESTS_JSON="${REQUESTS_JSON:-requests/census_household_gb_eng.json}"
LOCUST_OPTS="${LOCUST_OPTS:-'-f locustfile.py --no-web -c 800 -r 10 --loglevel=CRITICAL --run-time=2h --only-summary'}"

helm tiller run \
    helm upgrade --install \
    runner-benchmark \
    k8s/helm \
    --set host=${HOST} \
    --set requestsJson=${REQUESTS_JSON} \
    --set locustOptions=${LOCUST_OPTS} \
    --set image.repository=${DOCKER_REGISTRY}/eq-survey-runner-benchmark \
    --set image.tag=${IMAGE_TAG}