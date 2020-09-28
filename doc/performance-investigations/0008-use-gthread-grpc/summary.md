# Title

Gevent is currently in experimental status within the Google client libraries; the impact of switching to gthread as a gunicorn worker type has been investigated, as this is formally supported. Additionally, the gRPC protocol as an alternative to HTTP for Datastore has been investigated. This cannot currently be used with the gevent worker type.

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

| Metric              | baseline | gthread & grpc | gthread |
| ------------------- | -------- | -------------- | ------- |
| Questionnaire GETs  | 111ms    | 87ms           | 133ms   |
| Questionnaire POSTs | 109ms    | 132ms          | 128ms   |
| All requests        | 110ms    | 116ms          | 131ms   |


## Discussion

The results show very little difference between the `gevent` and `gthread` worker types in terms of performance. Errors remained at 0 for both. Switching to `gRPC` was also succesful, in so much that it worked, did not introduce errors and resulted in slightly better response times, especially for GET requests.

## Decision

1. The eq-questionnaire-runner web server, worker type, and worker threads variables should be made configurable via Concourse pipeline deployment and Helm charts.
1. Further testing of `gthread` and `grpc` should be undertaken, though under a substantially increased load.
1. The use of Datastore instead of Redis should be investigated, especially since the use og gRPC is possible using the `gthread` worker type.
