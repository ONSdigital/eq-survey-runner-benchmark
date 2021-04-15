# Upgrade Python from 3.8 to 3.9

Python's latest minor release version is 3.9. EQ Census is currently running on version 3.8, whereas the post-census branch has been upgraded to 3.9. This looks at possible performance improvements due to the upgrade.

## Benchmark profile

| Option                 | Value                        |
| ---------------------- | ---------------------------- |
| Requests file          | census_household_gb_eng.json |
| Run time               | 60m                          |
| User wait time minimum | 1                            |
| User wait time maximum | 2                            |
| Clients                | 100                          |
| Hatch rate             | 100                          |
| Number of workersi     | 7                            |
| Number of threads      | 7                            |

## Results

Results based on 99th percentile timings.

| Metric              | Baseline | Investigation |
| ------------------- | -------- | ------------- |
| Questionnaire GETs  | 198ms    | 154ms         |
| Questionnaire POSTs | 299ms    | 250ms         |
| All requests        | 247ms    | 202ms         |

## Decision

The upgrade has already merged, but this result shows a performance improvement when using Python 3.9 over Python 3.8.
