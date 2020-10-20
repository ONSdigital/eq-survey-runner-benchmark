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

Results based on 99th percentile timings.

| Metric | Baseline | Investigation |
|--------|----------|--------------|
| Questionnaire GETs | 333ms | 340ms|
| Questionnaire POSTs | 374ms| 379ms|
| All requests | 353ms | 359ms |
| Total requests (over 20 mins) | 750,432 | 746,720 |

Both the baseline and investigation tests saw the following

- 10 Runner instances (30 cores)
- ~650 rps
- ~3,600 launches and ~3,200 submissions (across 20 mins)
- baseline used an average of 14 cores
- investigation used an average of 16 cores

## Decision

While the latencies detailed above are similar (suggesting a merge is appropriate) it should be noted that the impact was seen in total CPU utilised to serve the tests (14 cores v 16 cores). Subsequent testing on a single instance of runner indicates that using Datastore over Redis for eq-session increases each request by ~40ms.

## Next steps if merged

- Stress tests with threaded web server architecture (over GRPC/HTTP)
- Strategy for deling with expired eq-session objects in Datastore
- Communicate these changes and revisit recent soak/nmax performance testing  
