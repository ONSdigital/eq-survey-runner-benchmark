# Launch by schema url performance investigation

This investigation was carried out to compare running the benchmark by launching the `test_benchmark_business` schema via the `url` vs launching by `schema name` as we do currently.

## Benchmark version

| Tag | Commit |
|--------|-------|
| v1.8.0  | 41f4b36a8712a502e3bd336167cac0344f1f1833

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | test_benchmark_business.json |
| Run time | 20 min |
| User wait time minimum | 1 |
| User wait time maximum | 2 |
| Clients | 50 |
| Hatch rate | 50 |
| Locust Instances | 1 |


## Results

| Run                                          | Requests per second | GETs (99th) (ms) | POSTs (99th) (ms) | 99th percentile Max CPU Usage (%) | Total Requests | Total Failures | Outputs                                              |  
|----------------------------------------------------------|---------------------|------------------|------------------------|-----------------------------------|----------------|----------------|------------------------------------------------------|  
| Baseline (Launch by schema name)    | 55.08              | 540             | 135                  | 35.0                              | 66,100         | 0              | [outputs](outputs/baseline/2022-05-31T09:55:47)      |
| Launch by Schema URL - Run 1    | 55.24              | 192             | 145                  | 34.0                              | 66,290         | 0              | [outputs](outputs/investigation/2022-05-31T10:48:15)      |
| Launch by Schema URL - Run 2    | 55.43              | 191             | 136                  | 35.0                              | 66,520         | 5              | [outputs](outputs/investigation/2022-05-31T11:18:01)      | 
| Launch by Schema URL - Run 3    | 55.51              | 189             | 131                  | 36.0                              | 66,613         | 0              | [outputs](outputs/investigation/2022-05-31T12:47:38)      | 

## Errors and Failures

- Launch by Schema URL - Run 2:
    - 5 x "Expected a (200) but got a (0) back when getting page"

The baseline run is in-line with the kinds of results we see from our daily performance test, where we are frequently getting 99th percentile response times of around 400ms. Launching by schema URL appeared to produce consistent results with significantly lower 99th percentile response times (around 160ms). The difference being, in the overnight daily-test and the baseline run here
the `GET` request to `introduction-block` often has high response times, whereas in the runs launching by schema url times were consistently below 300ms.