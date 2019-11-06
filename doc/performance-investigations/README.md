# Performance Investigations

## Creating a new investigation

1. Create a new folder for the investigation named `0000-descriptive-name-for-investigation` incrementing `0000` from the last used number.
2. Copy `TEMPLATE.md` into the directory as `summary.md`.
3. Update the template as appropriate.
4. Capture baseline metrics - `./run.sh requests/<requests_file> https://<runner_url> <duration> baseline`.
5. Deploy the investigation branch.
6. Capture metrics - `./run.sh requests/<requests_file> https://<runner_url> <duration> investigation`.
7. Copy the generated CSVs into the investigation folder.
8. Update `summary.md` with the results.

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
