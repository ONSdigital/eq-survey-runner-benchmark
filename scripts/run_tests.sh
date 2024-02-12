#!/bin/bash
#
# Run unit tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests.sh
set -o pipefail

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

py.test --cov-config=.coveragerc --cov --cov-report html

display_result $? 3 "Unit tests"
