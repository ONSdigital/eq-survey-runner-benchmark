# Use gthread gunicorn worker and grpc protocol

This investigation examines the feasibility of switching the gunicorn worker type from gevent to gthread, and the use of the gRPC protocol over HTTP when calling Datastore. There are a number of reasons for this investigation:

1. gevent is currently in experimental status within the Google gRPC client libraries.
1. gthread is fully supported by the Google cloud client libraries.
1. The Python PubSub library does not support HTTP and only works over gRPC.


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
| Worker Threads         | 10                           |

## Results

Results based on average timings.

| Metric              | baseline | gthread | gthread & gRPC |
| ------------------- | -------- | ------- | -------------- |
| Questionnaire GETs  | 111ms    | 133ms   | 87ms           |
| Questionnaire POSTs | 109ms    | 128ms   | 132ms          |
| All requests        | 110ms    | 131ms   | 116ms          |

## Discussion

The benchmark performance under gthread and gRPC are good enough to warrant further investigation. Response times increased under gthread (without gRPC) for both GET and POST requests by 20% over the baseline. Enabling gRPC however improved GET request response times by 24%, offset by an increase in POST request response times of 26%. As most requests in runner are a combination of a POST and then a GET, this should make little difference in real-world usage. Errors remained at 0 for both the gthread and the gthread & gRPC scenarios.

## Decision

1. Further testing of gthread and gRPC should be undertaken, though under a substantially increased load.
1. The eq-questionnaire-runner web server, worker type, and worker threads variables should be made configurable via Concourse pipeline deployment and Helm charts.
