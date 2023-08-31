# Python 3.11.4 Upgrade investigation

EQ Questionaire Runner is currently on `3.10.8` .
This investigation is to see the performance of Runner when upgraded to `3.11.4` compared to `3.10.8` .

https://github.com/ONSdigital/eq-questionnaire-runner/tree/upgrade-python-version-311

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | requests/test_benchmark_business.json|
| Run time | 20m |
| User wait time minimum | 1s |
| User wait time maximum | 2s |
| Clients | 50 |
| Hatch rate | 50 |

## Results

Results based on 99th percentile timings.
| Metric              | Baseline | Investigation |
| ------------------- | -------- | ------------- |
| Questionnaire GETs  | 827ms    | 826ms         |
| Questionnaire POSTs | 565ms    | 539ms         |
| All requests        | 730ms    | 720ms         |
| Total Requests      | 61,358   | 61,269        |
| Total Failures      | 0 .      | 0             |
| Error Percentage    | 0.0%     | 0.0%          |

## Decision

Merge
