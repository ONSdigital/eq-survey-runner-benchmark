# Feedback performance investigation

This test is to investigate the performance of business journey in comparison to the incumbent checkbox journey. No new requests file was generated as one was already present for `test_benchmark_business.json`.

## Benchmark version

| Tag | Commit |
|--------|-------|
| v1.8.0  | 41f4b36a8712a502e3bd336167cac0344f1f1833

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | test_benchmark_business.json |
| Run time | 20 min |
| User wait time minimum | 1 |
| User wait time maximum | 2 |
| Clients | 50 |
| Hatch rate | 50 |
| Locust Instances | 1 |

## Results

Results based on 99th percentile timings.

| Metric |  Investigation |
|--------|---------------|
| Questionnaire GETs | 220 |
| Questionnaire POSTs | 125 |
| All requests | 185 |
| Total requests (over 20 mins) | 466,591 |

Breakdown of benchmark business journey endpoints based on 99th percentile timings.

| Type | Name | Average response time |
|-----|----------------|----|
| GET | /questionnaire | 200 |
| GET | /questionnaire/block379/ | 100 |
| POST | /questionnaire/block379/ | 110 |
| GET | /questionnaire/block380/ | 110 |
| POST | /questionnaire/block380/ | 100 |
| GET | /questionnaire/block381/ | 99 |
| POST | /questionnaire/block381/ | 110 |
| GET | /questionnaire/block383/ | 97 |
| POST | /questionnaire/block383/ | 110 |
| GET | /questionnaire/block4616/ | 94 |
| POST | /questionnaire/block4616/ | 110 |
| GET | /questionnaire/block4952/ | 98 |
| POST | /questionnaire/block4952/ | 110 |
| GET | /questionnaire/block4953/ | 100 |
| POST | /questionnaire/block4953/ | 100 |
| GET | /questionnaire/introduction-block/ | 190 |
| POST | /questionnaire/introduction-block/ | 100 |
| GET | /questionnaire/submit/ | 95 |
| POST | /questionnaire/submit/ | 200 |
| GET | /session | 1200 |
| GET | /submitted/feedback/send | 96 |
| POST | /submitted/feedback/send | 170 |
| GET | /submitted/feedback/sent |93 |
| GET | /submitted/thank-you/ | 93 |
| GET | /submitted/view-response/ | 99 |


## Decision

Compared to checkbox journey that we use in daily tests, there is a substantial rise in response times on certain endpoints, `/session` being affected the most but to a lesser degree `/questionnaire/submit/` and `/submitted/view-response/`. It could be down to the fact that business journey is substantially bigger and more extensive than the checkbox one. No anomaly (or a way to remedy this) was discovered in Grafana dashboards charts and all other GET and POST request perform well so no further investigation is needed.
The benchmark business journey can be utilised for future daily performance tests.