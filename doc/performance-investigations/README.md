# Performance Investigations

## Creating a new investigation

1. Create a branch in runner prefixed with `performance-investigation` and make the proposed changes.
1. In this repo create a new folder named `0000-descriptive-name-for-investigation` incrementing `0000` from the last used number.
1. Copy `TEMPLATE.md` into the directory as `summary.md`.
1. Update `summary.md` as appropriate.
1. Capture baseline metrics - `./run.sh requests/<requests_file> https://<runner_url> <duration> baseline`.
1. Deploy the investigation branch.
1. Capture metrics - `./run.sh requests/<requests_file> https://<runner_url> <duration> investigation`.
1. Copy the generated CSVs into the investigation folder.
1. Update `summary.md` with the results.

## Extracting performance metrics from CSVs

You can use the `extract_distribution_summary.py` script to extract high level metrics from the Locust distributions CSV:

```
python extract_summary.py < baseline_distribution.csv
```

Will output something like:

```
Questionnaire GETs average: 220ms
Questionnaire POSTs average: 256ms
All requests average: 320ms
```
