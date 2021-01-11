# Gunicorn thread count configuration at scale

The previous [worker and thread count investigation](https://github.com/ONSdigital/eq-survey-runner-benchmark/blob/master/doc/performance-investigations/0013-gunicorn-worker-thread-config/summary.md) highlighted that we should do further testing at scale with a reduced number of threads. This test aims to:
- confirm that reducing the number of threads does not negatively impact performance across a varied load profile
- understand the impact on Redis connections

## Benchmark profile

| Option                             | Value                        |
|------------------------------------|------------------------------|
| Requests file                      | census_household_gb_eng.json |
| Run time                           | 20m x 5                      |
| User wait time minimum             | 1                            |
| User wait time maximum             | 2                            |
| Clients (per load injector)        | 200                          |
| Hatch rate (per load injector)     | 200                          |
| Number of workers                  | 7                            |
| Number of threads                  | 2, 3, 7 (current)            |
| Questionnaire Runner version       | v3.61.0                      |
| Questionnaire Runner min/max pods  | 50                           |

The load used was 10, 15, 20, 25, 30 load injectors, with each load run for 20 minutes.

## Results


| Number of threads | 50th | 90th | 95th | 99th | 99.9th | Total Requests | Redis Connections (peak) | 
| ----------------- | ---- | ---- | ---- | ---- | ------ | -------------- | ------------------------ |
| 2 | 84 | 248 | 377 | 970 | 1700 | 27,082,887 | 455 |
| 3 | 88 | 220 | 320 | 984 | 2094 | 27,135,561 | 489 |
| 7 | 96 | 254 | 383 | 1094 | 2478 | 26,666,848 | 645 |

### 99th percentile timings per load stage

| Number of injectors | 2 threads	| 3 threads	| 7 threads |
| ------------------- | ---------	| ---------	| --------- |
| 10 | 140 | 168 | 158 |
| 15 | 173 | 175 | 190 |
| 20 | 265 | 240 | 304 |
| 25 | 711 | 856 | 1385 |
| 30 | 2599 | 2499 | 2395 |

### 2 threads breakdown

| Load injector instances | 50th | 90th | 95th | 99th | 99.9th | GETs Average | POSTs Average | Total Requests |
| ----------------------- | ---- | ---- | ---- | ---- | ------ | ------------ | ------------- | -------------- |
| 10 | 55 | 88 | 103 | 140 | 201 | 128 | 153 | 2,956,643 |
| 15 | 61 | 104 | 124 | 173 | 250 | 161 | 185 | 4,389,345 |
| 20 | 70 | 137 | 171 | 265 | 431 | 255 | 275 | 5,743,555 |
| 25 | 91 | 255 | 367 | 711 | 1264 | 701 | 722 | 6,770,322 |
| 30 | 113 | 483 | 818 | 2599 | 4613 | 2586 | 2612 | 7,223,022 |

[Locust outputs](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-2020-01-11-seven-workers-two-threads/)

### 3 threads breakdown

| Load injector instances | 50th | 90th | 95th | 99th | 99.9th | GETs Average | POSTs Average | Total Requests |
| ----------------------- | ---- | ---- | ---- | ---- | ------ | ------------ | ------------- | -------------- |
| 10 | 60 | 102 | 121 | 168 | 241 | 152 | 185 | 2,925,626 |
| 15 | 63 | 107 | 126 | 175 | 260 | 161 | 189 | 4,377,001 |
| 20 | 74 | 136 | 164 | 240 | 397 | 225 | 256 | 5,734,824 |
| 25 | 93 | 216 | 299 | 856 | 2109 | 834 | 878 | 6,792,238 |
| 30 | 122 | 405 | 658 | 2499 | 5252 | 2473 | 2526 | 7,305,872 |

[Locust outputs](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-2020-01-11-seven-workers-three-threads/)

### 7 threads breakdown

| Load injector instances | 50th | 90th | 95th | 99th | 99.9th | GETs Average | POSTs Average | Total Requests |
| ----------------------- | ---- | ---- | ---- | ---- | ------ | ------------ | ------------- | -------------- |
| 10 | 59 | 97 | 114 | 158 | 234 | 143 | 173 | 2,934,219 |
| 15 | 65 | 112 | 134 | 190 | 282 | 172 | 208 | 4,358,995 |
| 20 | 79 | 155 | 193 | 304 | 541 | 274 | 336 | 5,670,734 |
| 25 | 101 | 252 | 355 | 1385 | 3649 | 1335 | 1436 | 6,588,228 |
| 30 | 137 | 486 | 825 | 2395 | 5208 | 2323 | 2469 | 7,114,672 |

[Locust outputs](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-2020-01-08-baseline)

## Observations

- Performance improved running fewer threads
- Two threads had the lowest timings for the higher percentiles
- Three threads had the lowest timings for the lower percentiles
- Three threads had the highest throughput (marginally better than two threads)
- There is a considerable reduction in Redis connections with less threads

## Decision

- Change all environments to use three threads
- Investigate reducing the number of workers
