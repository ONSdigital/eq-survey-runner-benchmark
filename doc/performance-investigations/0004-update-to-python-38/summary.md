# Update to Python 3.8

Following gevent now supporting Python 3.8 (as of gevent 1.5) we are now able to upgrade Python.
There will be performance implications with both Pythion 3.8 and the gunicorn/gevent.

https://github.com/ONSdigital/eq-questionnaire-runner/tree/update-to-python-38

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | |
| Run time | |
| User wait time minimum | |
| User wait time maximum | |
| Clients | |
| Hatch rate | |

## Results

Results based on 99th percentile timings.

| Metric | Baseline | Investigation |
|--------|----------|--------------|
| Questionnaire GETs | | |
| Questionnaire POSTs | | |
| All requests | | |

## Decision

Merge or discard?
