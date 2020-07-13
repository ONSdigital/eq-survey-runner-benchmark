# Scale Test June 2020

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
| 10 |3,100|79|112|0.0000|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T13:48:28)|
| 20 |6,300|158|120|0.0001 |[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T14:10:41)|
| 30 |9,500|235|110|0.0054|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T14:32:50)|
| 40 |12,800|315|110|0.0037|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T14:55:14)|
| 50 |16,000|395|110|0.0001|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T15:17:18)|
| 60 |19,200|467|110|0.0093|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T15:40:10)|
| 70 |22,400|553|110|0.0063|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T16:02:20)|
| 80 |25,600|647|112 |0.0014|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T16:24:29)|
| 90 |28,800|712|120|0.0027|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T16:47:18)|
| 100 |30,500|765|280|0.0065|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T17:09:28)|
| 110 |29,100|765|540|0.0067|[output](https://console.cloud.google.com/storage/browser/eq-stress-test-load-injectors-benchmark-outputs/stress-test/2020-06-26T17:31:39)|

- 600 Runner instances limit, 1800 (2400) vCPU available (3 of 4 cores)
- 523 Runner instances reached, 1596 (2092) vCPU requested, 781 vCPU used (49%)
- Error rate includes any HTTP status codes in the 400 and 500 range (neither are expected)
- The 99th percentile timings are the load balancer response times reported in Stackdriver

## Errors and Failures

- The total number of failures as reported by Locust across all requests was 11,142. This correlates with the errors we see in the load balancer and application logs and are detailed below
- 500 errors x 8 reported by the load balancer and application logs, all for the `/anyone-else-driving-question` (seen across 7 separate pods)
        
        File '/runner/app/forms/questionnaire_form.py', line 405, in generate_form
              form_data = _clear_detail_answer_field(form_data, question_schema)
        File '/runner/app/forms/questionnaire_form.py', line 381, in _clear_detail_answer_field
              for answer in question_schema['answers']:
        TypeError: 'NoneType' object is not subscriptable

- 500 errors x 3 (seen in isolation in one pod at 2020-06-26 18:33)
            
        requests.exceptions.ConnectionError: ('Connection aborted.', BrokenPipeError(32, 'Broken pipe'))
             
- 401 errors x 10,038 throughout (distributed across all pods)
        
        8,353 x flask_wtf.csrf.CSRFError: 400 Bad Request: The CSRF tokens do not match."
        2,028 x flask_wtf.csrf.CSRFError: 400 Bad Request: The CSRF session token is missing."

- 502 errors x 1,075 at 110 load injectors reported by load_balancer as `backend_timeout`

## Observations

- The run of 110 load injector instances saw a significant increase in response times resulting in request timeouts. This coincided with Redis reaching 100% CPU. At this point the load balancer began seeing the 502 `backend_timeout` errors
- The average submission rate in the 90 instances test was 135 responses per second, which is 486,000 responses per hour (assuming requests remain stable over an hour)
- 30,000 rps with 765 used vCPU is reasonable. This equates to 14.32 rps per core (as a GCP resource where the 4th core is effectively unusable). The test achieved 39 rps per core from the 765 vCPU being utilised at 30,000 rps

## Recommendations

- Runner is only utilising 49% of requested available vCPU. Test different gunicorn configurations and investigate other WSGI or event loop architectures
- Resolve/understand the 401 and 500 errors we have seen across this test
- Redis memorystore CPU 100%, test with increased spec to see if additional resource allows us to scale runner further
- Speak to GCP Redis engineers to understand this behaviour and if our usage is appropriate
- Tune and retest the kubernetes autoscaling and configuration (e.g is the 50% `target_cpu_utilization_percentage` appropriate)
- Update Grafana dashboard to add vCPU and Launch / Submission counts
- Update summary script to aggregate scale test results per folder more appropriately (inc. Total Requests, Failure %, Max response time)
