# Scale Test April 2020

## Benchmark settings
| Setting | Value |
| --- | ---| 
| Clients per instance | 200 |
| Clients hatch rate   | 200 |
| Wait time minimum | 1 |
| Wait time maximum | 2 |
| Requests JSON | census_household_gb_eng.json |
| Runtime | 20m |

## Results

| Load injector instances | Requests per second | CPU Usage (vCPU) | 99th percentile response time (ms) | Error rate (%) | Output |
| --- | --- | --- | --- | --- | --- |
| 70  | 21,600 | 990  | 220-240 | 0      | [output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-household-70/2020-04-17T10:36:14/) |
| 80  | 24,300 | 1160 | 275-295 | 0.0005 | [output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-household-80/2020-04-17T10:59:32/) |
| 90  | 25,500 | 1220 | 300-350 | 0.17   | [output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-household-90/2020-04-17T11:22:12/) |
| 90  | 27,000 | 1330 | 320-340 | 0      | [output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-household-90/2020-04-17T11:45:02/) |
| 100 | 28,000 | 1350 | 400-500 | 0.16   | [output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-household-100/2020-04-17T12:06:33/) |
| 100 | 28,000 | 1400 | 400-520 | 0.14   | [output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-household-100/2020-04-17T12:29:03/) |

- 600 instances, 2400 vCPU available, 1800 vCPU requested
- Error rate includes any HTTP status codes in the 400 and 500 range (neither are expected)
- The 99th percentile timings are the load balancer response times reported in Stackdriver

## Observations

- In the first run of 90 instances there was an increase in HTTP 502 errors.  These errors were reported by the load balancer as `backend_timeout`; as they were almost exclusively on POST requests it could be that Datastore was throttling writes while it scaled to cope with the surge in demand. This is not possible to prove as we don't have any timings for Datastore requests (they're not available in the Datastore Stackdriver metrics). Re-running the same test immediately a second time, no errors were observed.
- Both runs of 100 instances had increased error rates (HTTP 502). Again, as the errors were almost exclusively on POST requests, this could also have been be due to Datastore throttling writes. 
- The average submission rate in the 90 instances test was 114 responses per second, which is 410,000 responses per hour (assuming requests remain stable over an hour).

## Recommendations

- Speak to CATD and Google about the scaling of:
  - Kubernetes past the current default limit (2400 vCPU)
  - Datastore - how does it scale, both up and down, with demand
- Investigate how well the service copes in scaling up/down to meet demand
- Expose timing metrics for data requests - Redis and Datastore
- Investigate timeout settings to optimise response throughput
- Implement better ways to aggregate and visualise benchmark results
