#!/usr/bin/env bash

set -e

if [[ -z "$HOST" ]]; then
  echo "HOST is mandatory"
  exit 1
fi

DOCKER_REGISTRY="${DOCKER_REGISTRY:-eu.gcr.io/census-eq-ci}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

helm tiller run \
    helm upgrade --install \
    runner-benchmark \
    k8s/helm \
    --set host=${HOST} \
    --set image.repository=${DOCKER_REGISTRY}/eq-survey-runner-benchmark \
    --set image.tag=${IMAGE_TAG}