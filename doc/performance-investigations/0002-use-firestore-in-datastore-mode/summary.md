# Title

Current databases created via the Python Datastore library are traditional Datastore databases, Firestore offers a Datastore compatibility mode that reduces or removes some of the limitations of native Datatore.

See https://cloud.google.com/datastore/docs/firestore-or-datastore for more details.

Link to Github branch with proposed changes.

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | census_individual_gb_eng.json |
| Run time | 30m |
| User wait time minimum | 0 |
| User wait time maximum | 0 |
| Clients | 125 |
| Hatch rate | 125 |

## Results

Results based on 99th percentile timings.

| Metric | Baseline | Investigation |
|--------|----------|--------------|
| Questionnaire GETs | 1482ms | |
| Questionnaire POSTs | 1464ms| |
| All requests | 1700ms | |

## Decision

Merge or discard?
