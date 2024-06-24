# Enable HTML minification investigation

Minification of HTML was previously turned off due to performance issues before the Census. We need to investigate the
impact of re-enabling it in Runner.

Following on from a recent investigation of enabling HTML minification in Runner, we concluded that re-enabling
minification did not have any adverse affects on our
UI.

However, during the spike, we ran a basic performance benchmark to check if there were any performance impacts. We
now need to run a comprehensive performance investigation, to check the impact on our response rates and other key
indicators, such as our CPU usage, when minification is enabled. Enabling minification may have an adverse impact at a
larger scale.

## Runner settings

| Setting       | Value   |
|---------------|---------|
| Concurrency   | 115     |
| Max instances | 3       |
| Min instances | 3       |
| CPU           | 4       |
| Memory        | 4G      |
| Version       | v14.3.2 |

## Benchmark profile

Attempted to mimic traffic as closely as possible during a busy period for Runner. To avoid hitting Runner with a lot of
traffic on a 'cold start' against idle instances, the hatch rate was set to 5.

| Option                 | Value                                 |
|------------------------|---------------------------------------|
| Requests file          | requests/test_benchmark_business.json |
| Run time               | 20m                                   |
| User wait time minimum | 1s                                    |
| User wait time maximum | 3s                                    |
| Clients                | 80                                    |
| Hatch rate             | 5                                     |

## Results

No errors were present in any of the test runs, so have been excluded from the results

| Metric                                | Baseline | Investigation 1 | Investigation 2 | Investigation 3 |
|---------------------------------------|----------|-----------------|-----------------|-----------------|
| Questionnaire GETs (99th percentile)  | 267ms    | 274ms           | 265ms           | 261ms           |
| Questionnaire POSTs (99th percentile) | 238ms    | 248ms           | 251ms           | 252ms           |
| Total Requests                        | 86,409   | 86,023          | 86,370          | 86,308          |
| CPU Usage                             | 16.93%   | 18.61%          | 19.59%          | 19.79%          |
| Memory Usage                          | 31.98%   | 31.51%          | 31.80%          | 32.12%          |

Performance graphs:

* [baseline](outputs/baseline/performance_graph.png)
* [investigation](outputs/investigation/performance_graph.png)

## Observations

* Most noteworthy observation here is the CPU usage. Although it's only ~2% higher, enabling HTML minify seems to have a
  consistently higher CPU rate.

* The memory usage was consistent across all baseline and investigation runs, at ~30%

## Decision

Although negligible, enabling minify HTML seems to have a negative impact on CPU. It also doesn't appear to offer
any notable performance improvement
