# Stress Test December 2021
This is an initial stress test to asses the performance of runner after the switch from Kubernetes to Cloud Run. Below are the initial settings we used:


## Runner settings

| Setting | Value |
| --- | ---| 
| Concurrency | 250 |
| Max instances   | 1 |
| Min instances | 1 |


## Benchmark settings

| Setting | Value |
| --- | ---| 
| Load injector instances | 1 |
| Clients hatch rate   | 50 |
| Wait time minimum | 1 |
| Wait time maximum | 2 |
| Requests JSON | test_benchmark_business.json |
| Runtime | 10m |

## Results

| Clients per instance | Requests per second | 99th percentile Max CPU Usage (%) | 99th percentile response time (ms) | Error rate (%) | Output |
| --- | --- | --- | --- | --- | --- |
| 50  | 59.63 | 32.0  | 140 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T09:23:30) |
| 60  | 71.52 | 37.0  | 140 | 0.006 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T13:39:53) |
| 70  | 83.16 | 43.0  | 150 | 0.008 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T14:03:46) |
| 80  | 94.70 | 50.0  | 150 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T14:23:23) |
| 90  | 106.09 | 56.0 | 170 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T14:42:00) |
| 100 | 117.17 | 61.0 | 180 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T14:57:02) |
| 110 | 127.20 | 68.0 | 260 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T15:29:57) |
| 120 | 135.18 | 75.0 | 390 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T15:49:24) |
| 130 | 138.15 | 80.0 | 500 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-09T09:42:03) |
| 140 | 140.66 | 81.0 | 630 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-09T10:14:49) |
| 150 | 130.13 | 81.0 | 990 | 0.001 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-09T10:32:16) |
| 160 | 135.59 | 99.0 | 740 | 0.005 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-09T10:52:38) |

- The 99th percentile max cpu usage as reported in Grafana

## Errors and Failures

- 60 Clients per instance:
    - 4 x "Expected a (200) but got a (0) back when getting page"
- 70 Clients per instance:
    - 4 x "Expected a (200) but got a (0) back when getting page"
    - 1 x "Expected a (302) but got a (0) back when getting page"
- 150 Clients per instance:
  - 1 x "Expected a (302) but got a (0) back when getting page"
- 160 Clients per instance:
  - 3 x "Expected a (200) but got a (0) back when getting page"  

## Observations

- Some early errors that didn't persist when we increased the load.
- The following CPU usage thresholds were exceeded:
  - 50% at 80 clients per instance.
  - 60% at 100 clients per instance.
  - 70% at 120 clients per instance.
  - 80% CPU at 130 clients per instance.
  - 90% CPU at 160 clients per instance.
- Significant performance degradation on 99th percentile response time between 100 and 110 clients per instance.
- We reached over 300ms response on 99% at 120 clients per instance.
- Above 130 clients per instance CPU levels off because response times are degrading significantly.
- Even at 60-75% CPU, the response time is still performant.
- Above 150 clients per instance performance degradation is severe.
- Over the course of the test there were 42k survey submissions.

#Additional tests
Following our initial stress test we decided to run an additional test to prove that performance stays on similar levels when we fine tune runner's concurrency. Based on the table above we made an assumption that if we set concurrency to 90 we should get similar results. In addition, if we update number of min. max instances to 2 and double the number of clients per instance we should also obtain similar results.

##Comparison

| Clients per instance | Concurrency | Min. Max. instances | Requests per second | 99th percentile Max CPU Usage (%) | 99th percentile response time (ms) | Error rate (%) | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 90  | 250 | 1 | 106.09 | 56.0 | 170 |  0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-08T14:42:00) |
| 90  | 90 | 2 | 105.74 | 38.0 | 160 | 0.000 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-09T14:30:33) |
| 90  | 90 | 1 | 104.21 | 66.0 | 190 | 0.001 | [output](https://console.cloud.google.com/storage/browser/eq-stress-injector-07122021-outputs/stress-test/2021-12-09T13:39:52) |


## Observations

- When we fine-tuned runner's concurrency to be 90 and only one instance, the performance was slightly worse than we would expect (66% CPU usage compared to 56%). However, when we used 90 with 2 instances the performance significantly improved (e.g. CPU usage decreased and latency improved).