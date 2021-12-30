# Stress Test Phase 2 December 2021

Following the December 2021 phase 1 concurrency test we now need to scale test to ensure Runner is scaling linearly under Cloud Run.

The test intends to confirm that the observations in phase 1 are linear at scale (at 50 instances).

## Runner settings

| Setting | Value |
| --- | ---| 
| Concurrency | 115 |
| Max instances   | 50 |
| Min instances | 50 |
| CPU | 4 |
| Memory | 4G |
| Version | 3.89.0 |


## Benchmark settings

| Setting | Value |
| --- | ---| 
| Clients per instance | 100 |
| Clients hatch rate   | 50 |
| Wait time minimum | 1 |
| Wait time maximum | 2 |
| Requests JSON | test_benchmark_business.json |
| Runtime | 20m |

## Initial Benchmark

Prior to scaling runner to 50 instances, we ran an initial benchmark against runner 1 instance to check that the results were comparable with the phase 1 test.

For our phase 2 benchmark, the 99th percentile response time was slightly above our expected range of 140 to 180ms but the results were broadly similar to our phase 1 test. CPU usage peaked at 70% but for the most part stayed between 66-68%.

| Stress Test |Runner Concurrency |Runner Instances | Run Time| Clients per instance | Requests per second | 99th percentile Max CPU Usage (%) | 99th percentile response time (ms) | Error rate (%) | Output |
| --- | --- | --- | --- |--- | --- | --- | --- | --- | --- |
| Phase 2 | 115 | 1 | 20 mins | 100  | 116.40 | 70  | 190 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-23T11:34:57) |
| Phase 1 | 90 | 1 | 10 mins | 90  | 104.21 | 66  | 190 | 0.001 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-09T13:39:52)|


## Results

| Load Injector Instances | Requests per second | 99th percentile Max CPU Usage (%) | 99th percentile response time (ms) | Error rate (%) | Output |
| --- | --- | --- | --- | --- | --- |
| 1  | 116 | 49.5  | 210 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T08:29:18) |
| 5  | 488 | 11.5  | 3761 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T09:14:38) |
| 10  | 1173  | 35.5  | 157 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T10:07:10) |
| 15  |  1755 | 38.5  | 191 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T11:12:52) |
| 20  | 2330  |  32.8 | 399 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T11:49:25) |
| 25  |  2932 | 40.5  | 148 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T12:45:40) |
| 30  |  3507 |  51.5 | 178 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T13:24:05) |
| 35  |  4092 | 60.5  | 190 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T13:59:13) |
| 40  |  4668 | 64.5  | 229 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T14:42:36) |
| 45  | 5228 |  69.5 | 438 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T15:13:01) |
| 50  | 1789 | 93.5  | 42127 | 0.240 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-29T15:38:08) |

## Errors and Failures

- 30 load injector instances:
  - 1 x 500 error:
    `raise common.InvalidResponse("google.resumable_media.common.InvalidResponse: ('Request failed with status code', 503, 'Expected one of', <HTTPStatus.OK: 200>)`
- 35 load injector instances:
  - 3 x `Expected a (302) but got a (0) back when posting page`
- 50 load injector instances:
  - 1583 x 429 errors:
      `The request was aborted because there was no available instance.`
  - 1314  x 500 errors:
      `The datastore operation timed out, or the data was temporarily unavailable.','grpc_status':4}`
  - 2995 x 504 errors :
      `The request has been terminated because it has reached the maximum request timeout. To change this limit, see https://cloud.google.com/run/docs/configuring/request-timeout`


## Observations

### Overall:

- Runs between 1 and 20 load generator instances did not follow the expected linear pattern from the phase 1 test due to a number of spikes in CPU usage and backend latency.
- Runs between 25 and 40 load generator instances followed the expected linear pattern from the phase 1 test for 99th percentile response time and CPU usage and were generally more stable.
- Performance began to degrade significantly at 45 load generator instances.
- The application was fairly volatile throughout the test, observed many spikes in response times and CPU usage that did not occur in the phase 1 test.
- At 50 load injector instances the application began to fail, and thousands of `429` and `500` errors were observed. 

### Run by run:

- 1 load injector instance:
    - CPU usage remained low throughout the test at around 2.5% despite a significant spike to 49.5% toward the end of the test.
- 5 load injector instances:
    - Initially all stats looked healthy, CPU around 9% and response times at around 150ms as reported in grafana.
    - However, 13 minutes into the test saw a huge spike in response times (showing on grafana as 45s)  and application requests dropped to around ~125/s.
    - No obvious errors identified - potentially an issue with the load generator.
    - Despite the above issues, CPU usage remained consistent throughout.
- 10 load injector instances:  
    - Brief spike in CPU to 35% but for the majority of the test was level at around 17%.
    - Backend latency noticeably better than the first two runs.
- 15 load injector instances:  
    - Brief spike in CPU to 38% but for the majority of the test was level at around 25%.
    - Response time spiked twice to around 900ms which drove up the overall average.
- 20 load injector instances:  
    - 99th percentile CPU usage remained fairly stable at around 32% for the duration of the test.
    - Significant increase in backend latency compared with previous two runs driven by two spikes to over 1000ms.
- 25 load injector instances:  
    - CPU usage remained stable throughout the test.
    - Improved backend latency when compared with previous runs as there were less significant spikes.
- 30 load injector instances:  
    - CPU usage remained stable throughout the test.
    - Fewer significant spikes in backend latency.
- 35 load injector instances:
    - CPU usage remained relatively stable throughout the test.
    - A handful of spikes in backend latency.
- 40 load injector instances:
    - CPU usage remained relatively stable throughout the test.
    - A handful of spikes in backend latency.
- 45 load injector instances:
    - CPU usage remained relatively stable throughout the test.
    - A couple of large backend latency spikes to around 1s.
- 50 load injector instances:
  - Began to see a number of `429`/`Too many requests` errors at the beginning of the test.
  - This was followed by thousands of `500` errors at which point the test began to fail.
  - Response times reached over 5 mins (as reported in Grafana) and requests per second dropped to 0.
  - The app began to recover after 10 minutes without serving requests, and reached 5k req/s but CPU peaked at 93.5%.
  