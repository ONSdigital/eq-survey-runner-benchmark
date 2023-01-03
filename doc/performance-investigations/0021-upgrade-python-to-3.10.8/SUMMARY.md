# Python 3.10.8 Upgrade investigation

EQ Questionaire Runner is currently on `3.9` .
This investigation is to see the performance of Runner when upgraded to `3.10.8` compared to `3.9` .

https://github.com/ONSdigital/eq-questionnaire-runner/tree/upgrade-python-3.10.8

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
| Questionnaire GETs  | 638ms    | 468ms         |
| Questionnaire POSTs | 753ms    | 161ms         |
| All requests        | 681ms    | 354ms         |
| Total Requests      | 65,122   | 65,962        |
| Total Failures      | 40       | 0             |
| Error Percentage    | 0.06%    | 0.0%          |

## Decision

Merge or discard?
