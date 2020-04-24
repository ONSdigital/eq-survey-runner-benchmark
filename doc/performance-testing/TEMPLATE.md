# Title

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
|   |  |   |  |  | [output](<link to output bucket>) |

- 600 instances, 2400 vCPU available, 1800 vCPU requested
- Error rate includes any HTTP status codes in the 400 and 500 range (neither are expected)
- The 99th percentile timings are the load balancer response times reported in Stackdriver

## Observations

- List of important observations

## Recommendations

- List of recommendations