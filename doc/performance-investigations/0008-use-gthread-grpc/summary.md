# Use gthread gunicorn worker and grpc protocol

This investigation examines the feasibility of switching the gunicorn worker type from gevent to gthread, and the use of the gRPC protocol over HTTP when calling Datastore. There are a number of reasons for this investigation:

1. gevent is currently in experimental status within the Google client libraries.
1. gthread is fully supported by the Google cloud client libraries.
1. gRPC is not interoperable with the gevent worker type.
1. PubSub does not support HTTP.

Given the above, full interoperability with the Google Cloud Platform services via gRPC should be possible when using a combination of gthread as a gunicorn worker type with gRPC as the transport protocol. What remains to be seen is whether there is an impact (either positive or negative) on performance benchmarks.

Branch used: https://github.com/ONSdigital/eq-questionnaire-runner/tree/performance-investigation-gthread-grpc

## Benchmark profile

| Option                 | Value                        |
| ---------------------- | ---------------------------- |
| Requests file          | census_household_gb_eng.json |
| Run time               | 20m                          |
| User wait time minimum | 1                            |
| User wait time maximum | 2                            |
| Clients                | 64                           |
| Hatch rate             | 64                           |

## Results

Results based on average timings.

| Metric              | baseline | gthread | gthread & gRPC |
| ------------------- | -------- | ------- | -------------- |
| Questionnaire GETs  | 111ms    | 133ms   | 87ms           |
| Questionnaire POSTs | 109ms    | 128ms   | 132ms          |
| All requests        | 110ms    | 131ms   | 116ms          |

## Discussion

Response times under gthread (without gRPC) increased for both GET and POST requests however, With gthread & gRPC results show a 24% decrease in GET request response times. Although promising it was offset by a rise in POST request response times of 26%. Errors remained at 0 for both the gthread and the gthread & gRPC scenarios.

## Decision

1. The eq-questionnaire-runner web server, worker type, and worker threads variables should be made configurable via Concourse pipeline deployment and Helm charts.
1. Further testing of gthread and gRPC should be undertaken, though under a substantially increased load.
