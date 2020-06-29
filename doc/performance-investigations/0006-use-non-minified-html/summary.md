# Use non-minified HTML

The latest daily test highlights the time taken to minify the HTML output as one of the top 5 in terms of proportion of the request time. Given that we gzip the response, the effect of HTML minification is minimal. 

Notes
---
There are a few Jinja environment settings we can set to remove some of the [whitespace](https://jinja.palletsprojects.com/en/2.11.x/templates/#whitespace-control) from the output HTML:

```
application.jinja_env.trim_blocks = True
application.jinja_env.lstrip_blocks = True
```

Locust only shows raw data sizes despite using gzip in the test client, but average content size is increased from 4630 bytes to 9039 without flags and 6830 bytes with.

## Benchmark version

| Tag | Commit |
|--------|-------|
| latest | 8f2b9fe14eb19e19140f18b0e5bee78f4dbcb1af

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | census_household_gb_eng.json |
| Run time | 5 min |
| User wait time minimum | 0 |
| User wait time maximum | 0 |
| Clients | 100 |
| Hatch rate | 10 |

## Results

Results based on 99th percentile timings.

| Metric | Baseline | Investigation (Uncompressed) | Investigation (Jinja Flags) |
|--------|----------|--------------|
| Questionnaire GETs | 360 | 269 | 263 |
| Questionnaire POSTs | 446 | 377 | 320 |
| All requests | 490 | 390 | 330 |

## Decision

Merge or discard?
