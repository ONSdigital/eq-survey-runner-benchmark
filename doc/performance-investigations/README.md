# Performance Investigations

## Creating a new investigation

1. Create a branch in runner prefixed with `performance-investigation` and make the proposed changes.
1. Create a new folder in `doc/performance-investigations` named `0000-descriptive-name-for-investigation` incrementing `0000` from the last used number.
1. Copy `TEMPLATE.md` into the directory as `summary.md`.
1. Update `summary.md` as appropriate.
1. Capture baseline metrics using a given [configuration](#choosing-a-benchmark-configuration).
1. Deploy the investigation branch.
1. Capture metrics using the same configuration used in step 5.
1. Copy the generated CSVs (`baseline_*.csv`, `investigation_*.csv`) into the investigation folder.
1. Update `summary.md` with the results.

## Choosing a benchmark configuration

The simplest configuration to run is captured in `run.sh` which defaults to one client with no wait time:

```
./run.sh requests/<requests_file> https://<runner_url> <duration> <output_file_prefix>
```

`duration` can be in seconds (s), minutes (m), or hours (h). For example:

```
./run.sh requests/test_checkbox https://runner.co.uk 10m baseline
```

More in-depth configuration is explained in the top-level [Readme](/README.md).

## Extracting performance metrics from CSVs

You can use the `extract_distribution_summary.py` script to extract high level metrics from the Locust distributions CSV:

```
python scripts/extract_distribution_summary.py < baseline_distribution.csv
```

Will output something like:

```
Questionnaire GETs average: 220ms
Questionnaire POSTs average: 256ms
All requests average: 320ms
```
