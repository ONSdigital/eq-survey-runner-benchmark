# Use uWSGI server

We have only ever run the application with Gunicorn. We should try another web server to see if it is more performant, reliable or consistent.

https://github.com/ONSdigital/eq-questionnaire-runner/compare/add-uwsgi-option

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | census_household_gb_eng.json |
| Run time | 10m |
| User wait time minimum | 1 |
| User wait time maximum | 2 |
| Clients | 64 |
| Hatch rate | 64 |

This test replicates the current seetings for the daily test, but with a reduced runtime to allow for all of the variations to be tested in a reasonable time.

## Results

|                          | Request Count | Failure Count | Median Response Time | Average Response Time | Min Response Time | Max Response Time | Average Content Size | Requests/s | Failures/s |
|--------------------------|---------------|---------------|----------------------|-----------------------|-------------------|-------------------|----------------------|------------|------------|
| Gunicorn                 | 69424         | 0             | 50                   | 53.52                 | 14.66             | 2172.49           | 7846.93              | 115.77     | 0.000      |
| uWSGI 7 workers          | 70344         | 5             | 44                   | 47.01                 | 4.85              | 1425.64           | 7848.11              | 117.29     | 0.008      |
| uWSGI 15 workers         | 70441         | 2             | 42                   | 46.24                 | 5.17              | 2811.17           | 7850.25              | 117.45     | 0.003      |
| uWSGI threads 20 threads | 67741         | 12            | 54                   | 68.18                 | 5.76              | 4755.77           | 7838.74              | 112.95     | 0.020      |
| uWSGI threads 50 threads | 66104         | 15            | 58                   | 82.18                 | 5.46              | 7248.80           | 7833.27              | 110.22     | 0.025      |
| uWSGI async 20 cores     | 70140         | 3             | 47                   | 48.23                 | 7.51              | 445.25            | 7850.79              | 116.96     | 0.005      |
| uWSGI async 50 cores     | 70310         | 2             | 44                   | 47.33                 | 4.00              | 1460.57           | 7852.92              | 117.23     | 0.003      |

|                          | 50% | 66% | 75% | 80% | 90% | 95% | 98% | 99% | 99.90% | 99.99% | 100% |
|--------------------------|-----|-----|-----|-----|-----|-----|-----|-----|--------|--------|------|
| Gunicorn                 | 50  | 55  | 59  | 62  | 73  | 85  | 110 | 120 | 430    | 2000   | 2200 |
| uWSGI 7 workers          | 44  | 50  | 53  | 55  | 61  | 69  | 83  | 99  | 440    | 1300   | 1400 |
| uWSGI 15 workers         | 42  | 47  | 50  | 52  | 60  | 70  | 87  | 100 | 730    | 2600   | 2800 |
| uWSGI threads 20 threads | 54  | 65  | 74  | 82  | 110 | 140 | 190 | 230 | 1400   | 4300   | 4800 |
| uWSGI threads 50 threads | 58  | 73  | 87  | 99  | 140 | 190 | 260 | 320 | 2000   | 6600   | 7200 |
| uWSGI async 20 cores     | 47  | 52  | 55  | 57  | 64  | 73  | 91  | 110 | 200    | 350    | 450  |
| uWSGI async 50 cores     | 44  | 49  | 53  | 55  | 61  | 70  | 86  | 110 | 670    | 1200   | 1500 |

## Observations

- The timings for uWSGI without threads is better than Gunicorn, with lower higher percentile timings.
- The timing for threaded uWSGI seems high, but this could be due to configuring too many threads. Given the reasonable timings for the non-threaded UWSGI, we should try a smaller number of threads.
- The timings for uWSGI async 20 cores are far lower than everything else at the higher percentiles. 
- We haven't looked into the Gunicorn tuning options
- Gunicorn is the only option that didn't generate errors

## Decision

Merge. The changes allow runner to be configured to use either Gunicorn or uWSGI. Further testing should be carried out to determine which one works best for our use case, and what the appropriate settings are.
