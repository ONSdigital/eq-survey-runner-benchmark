# Use Redis for storing Questionnaire Runner sessions

The EQ session data are currently stored in Datastore. It may be more performant to store these data in Redis (which is already used for JWT).
https://github.com/ONSdigital/eq-questionnaire-runner/tree/performance-investigation-session-performance

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | census_household_gb_eng.json |
| Run time | 5m |
| User wait time minimum | 0 |
| User wait time maximum | 0 |
| Clients | 1 |
| Hatch rate | 1 |

| Option | Value |
|--------|-------|
| Requests file | census_household_gb_eng.json |
| Run time | 5m |
| User wait time minimum | 0 |
| User wait time maximum | 0 |
| Clients | 5 |
| Hatch rate | 5 |

| Option | Value |
|--------|-------|
| Requests file | census_household_gb_eng.json |
| Run time | 5m |
| User wait time minimum | 0 |
| User wait time maximum | 0 |
| Clients | 25 |
| Hatch rate | 25 |

| Option | Value |
|--------|-------|
| Requests file | census_household_gb_eng.json |
| Run time | 5m |
| User wait time minimum | 0 |
| User wait time maximum | 0 |
| Clients | 50 |
| Hatch rate | 50 |

## Results

### Baseline

| Clients, Hatch rate | GET Average (ms) | POST Average (ms) | All requests average (ms) |
| 1, 1 | 103 | 123 | 410 |
| 5, 5 | 138 | 157 | 270 |
| 25, 25 | 462 | 416 | 1200 |
| 50, 50 | 928 | 997 | 1600 |

### Investigation

| Clients & hatch rate | GET Average (ms) | POST Average (ms) | All requests average (ms) |
| 1, 1 | 95 | 110 | 490 |
| 5, 5 | 121 | 141 | 280 |
| 25, 25 | 353 | 422 | 570 |
| 50, 50 | 387 | 451 | 550 |

## Results

Performance with Datastore degrades more quickly than Redis as the number of client connections increases.

## Decision

Merge.
