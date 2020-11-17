# Stress Test November 2020

A stress test was carried out on November 12th 2020 to test changes made since the last test. The aim of these changes was to reduce errors and increase the maximum requests that can be served:
- Sessions are now in Datastore (previously Redis)
- The application runs using Gunicorn threads (previously Gunicorn async)
- As we are now using threads, Datastore is now using gRPC (previously HTTP)

Runner version: [v3.54.0](https://github.com/ONSdigital/eq-questionnaire-runner/releases/tag/v3.54.0)

Infrastructure version: [v2.1.0](https://github.com/ONSdigital/eq-terraform-gcp/releases/tag/v2.1.0)

Benchmark version: [v1.0.0](https://github.com/ONSdigital/eq-survey-runner-benchmark/releases/tag/v1.0.0)

## Benchmark settings

| Setting | Value |
| --- | ---| 
| Clients per instance | 200 |
| Clients hatch rate   | 200 |
| Wait time minimum | 1 |
| Wait time maximum | 2 |
| Requests JSON | census_household_gb_eng.json |
| Runtime | 20m |

## Results

| Load injector instances | Requests per second | CPU Usage (vCPU) | 99th percentile response time (ms) | Error rate (%) | Output |
| --- | --- | --- | --- | --- | --- |
| 60  | 19,000 | 390  | 135  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T13:12:07)|
| 70  | 22,000 | 450  | 135  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T13:34:38/)|
| 80  | 25,000 | 520  | 135  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T13:56:58/)|
| 90  | 28,500 | 580  | 135  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T14:19:57/)|
| 100 | 31,500 | 650  | 135  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T14:43:17/)|
| 110 | 35,000 | 720  | 135  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T15:05:19/)|
| 120 | 38,000 | 780  | 135  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T15:27:28/)|
| 130 | 41,000 | 850  | 135  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T15:49:57/)|
| 140 | 44,500 | 920  | 140  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T16:12:18/)|
| 150 | 47,500 | 990  | 145  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T16:34:47/)|
| 160 | 50,000 | 1070 | 155  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T16:57:27/)|
| 170 | 53,500 | 1150 | 175  | 0.00000009 (6) |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T17:20:17/)|
| 180 | 56,500 | 1220 | 195  | 0.0000003 (15) |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T17:42:51/)|
| 190 | 59,500 | 1300 | 230  | 0.0000002 (12) |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T18:06:27/)|
| 200 | 63,000 | 1390 | 270  | 0.0000002 (17) |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T18:29:30/)|
| 210 | 65,000 | 1460 | 320  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T18:51:57/)|
| 220 | 67,500 | 1530 | 390  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T19:14:59/)|
| 230 | 70,000 | 1600 | 500  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T19:37:18/)|
| 240 | 72,000 | 1660 | 750  | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T19:59:47/)|
| 250 | 74,000 | 1710 | 1000 | 0 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test-november-2020/2020-11-12T20:22:28/)|

- Error rate includes any HTTP status codes in the 400 and 500 range (neither are expected)
- The 99th percentile timings are the load balancer response times reported in Stackdriver
- Over the course of the test 1,155,579,786 requests were made, 5.2 million launches and 4.6 million submissions

## Errors and Failures

- 815 errors reported by Locust:
  - 46 x "Expected a (200) but got a (0) back when getting page"
  - 9 x "Expected a (302) but got a (0) back when getting page" (`/session` and `/questionnaire`)
  - 710 x "Expected a (302) but got a (0) back when posting page"
  - 50 x "Expected a (302) but got a (500) back when posting page: /questionnaire/ with data"
- The zero status code errors from Locust are assumed to be from Locust issues
- 50 HTTP 500 errors reported in GCP (by the load balancer and application)
- All HTTP 500 errors happened when submitting to GCS, reported by the application logs as:
        
        "Traceback (most recent call last):",
        "  File '/usr/local/lib/python3.8/site-packages/flask/app.py', line 1950, in full_dispatch_request",
        "    rv = self.dispatch_request()",
        "  File '/usr/local/lib/python3.8/site-packages/flask/app.py', line 1936, in dispatch_request",
        "    return self.view_functions[rule.endpoint](**req.view_args)",
        "  File '/runner/app/helpers/session_helpers.py', line 19, in wrapped_function",
        "    return function(questionnaire_store, *args, **kwargs)",
        "  File '/runner/app/helpers/schema_helpers.py', line 25, in wrapped_function",
        "    return function(schema, *args, **kwargs)",
        "  File '/runner/app/routes/questionnaire.py', line 108, in get_questionnaire",
        "    submission_handler.submit_questionnaire()",
        "  File '/runner/app/views/handlers/submission.py', line 30, in submit_questionnaire",
        "    submitted = current_app.eq['submitter'].send_message(",
        "  File '/runner/app/submitter/submitter.py', line 39, in send_message",
        "    blob.upload_from_string(str(message).encode('utf8'))",
        "  File '/usr/local/lib/python3.8/site-packages/google/cloud/storage/blob.py', line 2437, in upload_from_string",
        "    self.upload_from_file(",
        "  File '/usr/local/lib/python3.8/site-packages/google/cloud/storage/blob.py', line 2220, in upload_from_file",
        "    created_json = self._do_upload(",
        "  File '/usr/local/lib/python3.8/site-packages/google/cloud/storage/blob.py', line 2052, in _do_upload",
        "    response = self._do_multipart_upload(",
        "  File '/usr/local/lib/python3.8/site-packages/google/cloud/storage/blob.py', line 1654, in _do_multipart_upload",
        "    response = upload.transmit(",
        "  File '/usr/local/lib/python3.8/site-packages/google/resumable_media/requests/upload.py', line 139, in transmit",
        "    response = _request_helpers.http_request(",
        "  File '/usr/local/lib/python3.8/site-packages/google/resumable_media/requests/_request_helpers.py', line 136, in http_request",
        "    return _helpers.wait_and_retry(func, RequestsMixin._get_status_code, retry_strategy)",
        "  File '/usr/local/lib/python3.8/site-packages/google/resumable_media/_helpers.py', line 165, in wait_and_retry",
        "    response = func()",
        "  File '/usr/local/lib/python3.8/site-packages/google/auth/transport/requests.py', line 464, in request",
        "    response = super(AuthorizedSession, self).request(",
        "  File '/usr/local/lib/python3.8/site-packages/requests/sessions.py', line 530, in request",
        "    resp = self.send(prep, **send_kwargs)",
        "  File '/usr/local/lib/python3.8/site-packages/requests/sessions.py', line 643, in send",
        "    r = adapter.send(request, **kwargs)",
        "  File '/usr/local/lib/python3.8/site-packages/requests/adapters.py', line 498, in send",
        "    raise ConnectionError(err, request=request)",
        "requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))"

## Observations

- As sessions are stored in Datastore again, Redis was under much less load. This was the main contributing factor to a request rate of double the previous limit reached (74,000 rps vs 34,000 rps). 
- Redis only reached a peak of 11% CPU usage and 6,400 connected clients.
- The error rate was very low. The errors happened in the middle of the test, for 4 of 20 test runs, after that there were 5 test runs with no errors. This may have been due to GCS scaling issues.
- The previous Datastore errors did not occur, this looks to have been fixed by switching from HTTP to gRPC for Datastore calls.
- Response times remained consistent until just over half of the allocated vCPU was used (900 of 1800 vCPU). Around this time the k8s cluster node scaling limit was reached.
- 99th percentile response times reached 1 second at 95% CPU usage.
- The `loadbalancing.googleapis.com/https/backend_request_count` 500 metric as reported in Grafana (81 errors) didn't align with the errors reported by the load balancer (50 errors).

## Recommendations

- Update all environments to use threads and gRPC
- Reduce the Redis instance size
- Investigate GCS retries
- Understand GCS scaling and speak to Google about the errors
- Investigate the load profile we use to more evenly distribute writes to GCS
- Test what happens when the application gets saturated; this could be done under lower load with a lower k8s node limit
- Test increasing the CPU allocation of the application and variations of k8s node size
- Improve HTTP 500 error alerts to be more specific
- Investigate how errors are reported in the GCP metric graphs to understand why they don't align with the log errors
- Consider automating the running of the stress test, manually increasing the load injectors and re-flying the pipeline every ~20 minutes is time consuming and error prone
- Improve the benchmark scripts to extract more insights from the Locust outputs