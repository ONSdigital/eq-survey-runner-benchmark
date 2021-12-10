# Relationship Test September 2020

## Purpose

To test the effect of relationship performance (response time), when increasing household members progressively up to 30.

## Test conditions

Using request file test_relationships.json and 2 new GCP instances built from our [pipeline repo](https://github.com/ONSdigital/eq-pipelines) ([daily test load injector](https://github.com/ONSdigital/eq-pipelines/tree/master/performance-testing/daily-test) and [development test environment](https://github.com/ONSdigital/eq-pipelines/tree/master/development/test)), household members were added using the list collector, relationship questions then answered, before being removed and the questionnaire submitted.

As a calibration excise, the new GCP instances were compared to the daily benchmark using census_household_gb_eng.json over 20 minutes.

**Latest Daily Performance Metrics (6th September 2020, taken from Slack)**

GETs average: 100ms
POSTs average: 125ms
All requests average: 112ms


**New instance**

GETs average: 100ms
POSTs average: 121ms
All requests average: 111ms

This confirmed that the new instance and load injector were configured and performing the same as the daily benchmark setup.


## Test settings

| Setting | Value |
| --- | ---|
| Clients per instance | 64 |
| Clients hatch rate   | 64 |
| Wait time minimum | 1 |
| Wait time maximum | 2 |
| Requests JSON | test_relationships.json |
| Runtime | 20m |
| last commit | [783f102e6fbeab11fbc221e9800143e2340ee09c](https://github.com/ONSdigital/eq-questionnaire-runner/commit/783f102e6fbeab11fbc221e9800143e2340ee09c)

## Results

| Household Members | GET (ms) | POST (ms) | Average (ms) |
|-------------------|----------|-----------|--------------|
| 5                 | 96       | 105       | 100          |
| 10                | 82       | 104       | 92           |
| 20                | 91       | 115       | 103          |
| 30 (1st test)     | 118      | 162       | 140          |
| 30 (2nd test)     | 114      | 150       | 132          |

- All results were recorded at the 99th percentile.
- Each test generated ≈135k requests.
- No errors or failures were recorded in any of the test.


## Observations

- Having 5/10 households members made no difference, and in fact returned slightly lower figures than the benchmark/calibrated results. I would put this down to natural deviation in testing and not worth further investigation.
- Having 20 members in a household had a slightly higher POST time, but it's marginal.
- Having 30 members in the household produced a clear increase in response times ≈20% for GETs and ≈30% for POSTs, this was significant enough for me to repeat the test, which returned the same findings.


## Recommendations

- Although there is a noticeable performance decrease going from 20 to 30 household members, I don't believe it's significant enough to recommend any changes aimed at optimizing how relationships work. Even at 30 household members I believe the response time is acceptable. If we did decide to make improvements, considering the amount of households it would affect, I would make it very low priority.
- Monitoring the performance of relationships regularly doesn't seem necessary, but might be nice to have. Relationship performance deviates only slightly from other block types, this doesn't warrant extra monitoring on its own, but could as a bigger piece if we were to split up major block types when reporting benchmark results.