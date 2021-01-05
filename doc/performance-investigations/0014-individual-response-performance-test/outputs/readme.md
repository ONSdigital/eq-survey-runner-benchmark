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

Overall Locust results based on 99th percentile timings.


| Metric | Baseline | Investigation |
|--------|----------|---------------|
| Questionnaire GETs | 153 | 96 |
| Questionnaire POSTs | 161 | 116 |
| All requests | 157 | 106 |
| Total requests (over 20 mins) | 1,276,602 | 1,212,989 |


Breakdown of Individual Response endpoints based on the average 99th percentile timings over the four runs.

| GET/POST | Endpoint|  Average (ms) |
|---------------------|------------------|-------------------|
| GET | /individual-response/?list_item_id={id} | 83 |
| GET | /individual-response/post/confirmation | 82 |
| POST | /individual-response/post/confirmation | 78 |
| GET | /individual-response/text/confirmation?mobile_number={id} | 79 |
| POST | /individual-response/text/confirmation?mobile_number={id} | 74 |
| GET | /individual-response/{id}/how | 91 |
| POST | /individual-response/{id}/how | 82 |
| GET | /individual-response/{id}/post/confirm-address | 89 |
| POST | /individual-response/{id}/post/confirm-address | 148 |
| GET | /individual-response/{id}/text/confirm-number?mobile_number={id} | 87 |
| POST | /individual-response/{id}/text/confirm-number?mobile_number={id} | 148 |
| GET | /individual-response/{id}/text/enter-number | 82 |
| POST | /individual-response/{id}/text/enter-number | 79 |


## Decision
Overall the individual response urls do not show any signs of poor performance, all get and posts requests showed better performance times than the baseline test using the household census schema.

Two Individual response POST requests show a significantly slower performance in comparison with the others, although these endpoints are where the telephone number and email address are entered, and the timings are in-line with the POST requests in the baseline tests.