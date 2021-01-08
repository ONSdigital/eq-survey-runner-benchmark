# Feedback performance investigation

This test is to investigate the performance of feedback journey. Limit of feedback submissions was extended to 5 to allow a single journey to exercise more than 2 feedback (to facilitate more requests with fewer launches/submissions). `census_household_gb_eng.json` journey was used as a baseline. New requests file was generated from `test_feedback.json` schema for this investigation.

## Benchmark version

| Tag | Commit |
|--------|-------|
| feedback-performance-investigation  | 38ae1812858d9b1a4d204fc336adad6a63831f1c

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | census_household_gb_eng.json |
| Run time | 30 min |
| User wait time minimum | 1 |
| User wait time maximum | 2 |
| Clients | 144 |
| Hatch rate | 144 |
| Locust Instances | 1 |

## Results

Results based on 99th percentile timings.

| Metric | Baseline | Investigation |
|--------|----------|---------------|
| Questionnaire GETs | 118 | 74 |
| Questionnaire POSTs | 141 | 121 |
| All requests | 129 | 86 |
| Total requests (over 20 mins) | 1,924,318 | 1,484,407 |

Breakdown of feedback journey endpoints based on 99th percentile timings.

| Type | Name | Average response time |
|-----|----------------|----|
| GET | /questionnaire | 91 |
| GET | /questionnaire/feedback/ | 100 |
| POST | /questionnaire/feedback/ | 120 |
| GET | /questionnaire/summary/ | 91 |
| POST | /questionnaire/summary/ | 185 |
| GET | /session | 240 |
| GET | /submitted/feedback/send | 67 |
| POST | /submitted/feedback/send | 108 |
| GET | /submitted/feedback/sent | 55 |
| GET | /submitted/thank-you/ | 59 |

## Decision

Compared to baseline, there is a significant drop in response times in feedback journey, all get and post request perform well so no further investigation is needed.
