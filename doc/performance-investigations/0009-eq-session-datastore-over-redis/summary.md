# eq-session in Datastore instead of Redis

Recent scale and stress testing has shown that using Memorystore Redis as the backend for eq-session with the current Runner and Redis architecture does not support the volume of requests required for upcoming Runner use cases.

This test is to investigate the impact of moving eq-session from Redis to Datastore under the current Runner v3.52.0 implementation and web server architecture (gunicorn-async with 7 workers)

https://github.com/ONSdigital/eq-questionnaire-runner/tree/performance-investigation-eq-session-datastore

## Benchmark profile

| Option                 | Value                        |
| ---------------------- | ---------------------------- |
| Requests file          | census_household_gb_eng.json |
| Run time               | 20m                          |
| User wait time minimum | 1                            |
| User wait time maximum | 2                            |
| Clients                | 200                          |
| Hatch rate             | 200                          |
| Locust Instances       | 2                            |

## Results

Locust results based on 99th percentile timings.

| Metric | Baseline | Investigation |
|--------|----------|--------------|
| Questionnaire GETs | 333ms | 340ms|
| Questionnaire POSTs | 374ms| 379ms|
| All requests | 353ms | 359ms |
| Total requests (over 20 mins) | 750,432 | 746,720 |

Environment monitoring observations

- 10 Runner instances (30 cores)
- ~650 rps
- ~3,600 launches and ~3,200 submissions (across 20 mins)

| Metric | Baseline | Investigation |
|--------|----------|--------------|
| Runner cores used (of 30) | 14 | 16|
| Redis connected clients | 345 | 127 |
| Redis CPU | 3.5% | 0.35% |

## Decision

While the Locust latencies detailed above are similar (suggesting a merge is appropriate) it should be noted that the main impact across 10 instances of Runner was seen in the total Runner CPU utilised (14 cores for the Redis baseline v 16 cores for the Datastore investigation). However, as expected Redis CPU is significantly improved when eq-session is in Datastore. 

Subsequent testing on a single instance of runner indicates that using Datastore over Redis for eq-session increases each eq-session request by ~40ms. This is consistent with previous observations of the two different backends.

Recommend merging given the current limitations at scale.

## Next steps if merged

- Update environments to downscale Redis instance
- Stress tests with threaded web server architecture (over GRPC/HTTP)
- Strategy for dealing with expired eq-session objects in Datastore
- Communicate these changes and revisit recent soak/N-Max performance testing  
- Allow eq-session `EQ_SESSION_BACKEND` to be specified by an environment variable as `storage` (default) or `ephemeral_storage`
