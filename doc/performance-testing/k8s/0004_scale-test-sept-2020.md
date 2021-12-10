# Scale Test September 2020

A September 2020 scale test was carried out against Runner v3.48.0 with eq-session in a 36GB Redis instance.

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
| 60 |18,500|398|109|0.00002|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-09-29T07:22:43)|
| 70 |21,500|470|115|0.00006|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-09-29T07:45:53)|
| 80 |24,500|535|112 |0.00003|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-09-29T08:07:56)|
| 90 |28,800|600|109|0.00003|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-09-29T08:30:03)|
| 100 |30,500|666|112|0.00002|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-09-29T08:52:07)|
| 110 |34,000|750|125|0.00007|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-09-29T09:14:23)|
| 120 |37,000|802|115|0.00004|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-09-29T09:37:14)|

- 600 Runner instances limit, 2400 vCPU available, 1800 vCPU usable (3 of 4 cores)
- 599 Runner instances reached, 1797 vCPU requested, 802 vCPU used (45%)
- Error rate includes any HTTP status codes in the 400 and 500 range (neither are expected)
- The 99th percentile timings are the load balancer response times reported in Stackdriver

## Errors and Failures

- There were 105 failures as reported by Locust across 232,232,087 requests
- The number of Locust failures (105) correlates with the errors we see in the load balancer and application logs and are detailed below
- HTTP 500 errors (105) reported by load_balancer as `statusDetails: "response_sent_by_backend"`
- HTTP 500 errors (92) reported by the application logs:
        
        77: "  File '/usr/local/lib/python3.8/site-packages/google/cloud/datastore/_http.py', line 70, in _request"
        78: "    response = http.request(url=api_url, method='POST', headers=headers, data=data)"
        85: "  File '/usr/local/lib/python3.8/site-packages/requests/adapters.py', line 498, in send"
        86: "    raise ConnectionError(err, request=request)"
        87: "requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))"

- HTTP 500 errors (13) reported by the application logs:

        89: "  File '/usr/local/lib/python3.8/site-packages/google/cloud/datastore/_http.py', line 70, in _request"
        90: "    response = http.request(url=api_url, method='POST', headers=headers, data=data)"
        97: "  File '/usr/local/lib/python3.8/site-packages/requests/adapters.py', line 498, in send"
        98: "    raise ConnectionError(err, request=request)"
        99: "requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))"

## Observations

- The run of 120 load injector instances saw no significant increase in response times
- At 37k rps Redis CPU reached 91% and allowed Runner to scale to 599 instances (past June scale test of 523 Runner instances). Increasing the Redis instance from 4GB TO 36GB saw ~15% improvement in Redis CPU consumption
- The average submission rate for our benchmark journey in the 120 instances test was 150 responses per second, which is 540,000 responses per hour (assuming requests remain stable over an hour)
- 37,000 rps at 802 used vCPU is 46 rps per core
- 37,000 rps at 1797 requested vCPU is 20.58 rps per core
- 37,000 rps at 2396 total vCPU is 15.44 rps per core

## Recommendations

- Redis memorystore is 91% CPU, test with eq-session in Datastore (over GRPC/HTTP)
- Tune and retest the Kubernetes autoscaling and configuration (e.g is the 50% `target_cpu_utilization_percentage` appropriate)
- Update summary script to aggregate 100% reponse times
- Add stackdriver alerts for resources (e.g. vCPU / Nodes)
- Due to time and resource constraints for this test, runner utilised only 45% of requested available vCPU. All future stress tests should increase load to the point where the utilised vCPU increases, identifying the corresponding response times and error rates
- Investigate the above datastore HTTP `Connection aborted` exceptions seen during the test
