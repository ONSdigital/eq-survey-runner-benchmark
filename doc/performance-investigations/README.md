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

Depending on the duration of the tests, you may want to consider running them more than once.

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
python scripts/extract_distribution_summary.py < baseline_stats.csv
```

Will output something like:

```
Questionnaire GETs average: 220ms
Questionnaire POSTs average: 256ms
All requests average: 320ms
```

## Proposed investigations

- Move session to Redis
- Use Firestore not in Datastore mode
- Update to Python 3.8
- Merge session into questionnaire state
- Clean view model passed to template reducing Python code executed from templates
- Work done in before request
- Per session CSRF token
- Gunicorn alternatives (uwsgi or gevent direct)
- Gunicorn (or alternative) tuning
- Authentication with Flask-Login (possible removal of Flask-Login)
- Alternative to simplejson e.g. orjson or rapidjson
- Encrypt questionnaire state and session directly rather than via JWE
- Configuration settings for client libraries e.g. Redis, Datastore
- Answer store structure performance - flat vs nested
- Don't encrypt progress store
- More in-memory caching of things that don't change per request
- Caching of method calls - can it be faster? - it looks like flask caching is using pickle
- Convert critical Python code to C using Cython
- Use PyPy