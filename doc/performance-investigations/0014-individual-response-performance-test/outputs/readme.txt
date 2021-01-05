# Individual Response Performance Investigation

This test was carried out  to investigate the performance of the individual response journey. A new `individual_response` requests file was generated for this test, it follows a happy path containing two individual response requests, one by telephone and one by post. The `census_household_gb_eng.json` journey was used as a baseline.

## Benchmark profile

| Option                 | Value                        |
| ---------------------- | ---------------------------- |
| Requests file          | census_individual_response.json |
| Run time               | 20m                          |
| User wait time minimum | 1                            |
| User wait time maximum | 2                            |
| Clients                | 144                         |
| Hatch rate             | 144                          |
| Locust Instances       | 1                            |

## Results

Locust results based on 99th percentile timings.

| Metric | Baseline | Investigation |
|--------|----------|---------------|
| Questionnaire GETs | 153 | 96 |
| Questionnaire POSTs | 161 | 116 |
| All requests | 157 | 106 |
| Total requests (over 20 mins) | 1,276,602 | 1,212,989 |


## Decision

The individual response urls do not show any signs of poor performance, all get and posts requests showed better performance times than the baseline test.