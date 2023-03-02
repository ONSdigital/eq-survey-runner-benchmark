
# Cloud Run gen2 execution environment   

[From GCP docs](https://cloud.google.com/run/docs/about-execution-environments)

>Cloud Run services by default operate within the first generation execution environment, which features fast cold start 
times and emulation of most, but not all operating system calls.  
Originally, this was the only execution environment available to services in Cloud Run but now second generation has 
been released by GCP and provides the following:
>- Faster CPU performance
>- Faster network performance
>- Full Linux compatibility
>- Network file system support

Runner’s current deployment makes use of the default first generation execution environment; this investigation looks 
at the use of second gen execution environment and the potential of any performance gain. 

Currently, we have a slack alert for `Load Balancer Backend Latency` check with a threshold of 0.75 sec. The PDF
generation endpoint is CPU intensive and is not as performant as the rest of the app which creates known latency
check alerts for PDF generation endpoint. 

This investigation specifically looks into the PDF generation endpoint and tries to evaluate if there would be any 
potential performance gain to avoid known `Load Balancer Backend Latency` check alert making use of second generation
execution environment.

## Runner settings

| Setting       | Value                                                                                                         |
|---------------|---------------------------------------------------------------------------------------------------------------|
| Concurrency   | 115                                                                                                           |
| Max instances | 3                                                                                                             |
| Min instances | 3                                                                                                             |
| CPU           | 4                                                                                                             |
| Memory        | 4G                                                                                                            |
| Commit        | [main](https://github.com/ONSdigital/eq-questionnaire-runner/commit/caff9b764cbc39fb846eeb3ad14e935dff3ac53a) |

## Benchmark profile

| Option                 | value                               |
|------------------------|-------------------------------------|
| Requests file          | test_business_benchmark_pdfkit.json |
| Run time               | 20m                                 |
| User wait time minimum | 1s                                  |
 | User wait time maximum | 2s                                  |
| Clients                | 50                                  |
| Hatch rate             | 50                                  |

## Results

### Execution Environment Performance

#### Results based on 99th percentile timings.

| Metric                                   | Baseline (gen1)                                                                    | Investigation (gen2)                                                                    |
|------------------------------------------|------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| **GET** <br/>(*/submitted/download-pdf*) | 1900ms                                                                             | 1400ms                                                                                  |
| Total Requests                           | 2,176                                                                              | 2,203                                                                                   |
| 99th percentile Max CPU Usage (%)        | 30.9%                                                                              | 28.0%                                                                                   |
| Total Failures                           | 0                                                                                  | 0                                                                                       |
| Error Percentage                         | 0.0%                                                                               | 0.0%                                                                                    |
| Results                                  | [benchmark_results](outputs/baseline/2023-02-27/Results_For_Latest_Benchmark.yaml) | [benchmark_results](outputs/investigation/2023-03-02/Results_For_Latest_Benchmark.yaml) |
| Performance Graph                        | [result](outputs/baseline/2023-02-27/performance_graph.png)                        | [result](outputs/investigation/2023-03-02/performance_graph.png)                        |

#### Detailed Results.

| Execution Environment | Type | Name                    | Request Count | Failure Count | Average Response Time(ms) | Average Content Size(B) | Requests/s | 50%  | 66%  | 75%  | 80%  | 90%  | 95%  | 98%  | 99%  | 99.90% | 99.99% | 100% | outputs                                     |
|-----------------------|------|-------------------------|---------------|---------------|---------------------------|-------------------------|------------|------|------|------|------|------|------|------|------|--------|--------|------|---------------------------------------------|
| Gen1                  | GET  | /submitted/download-pdf | 2176          | 0             | 1134.83901                | 352743.324              | 1.81477554 | 1100 | 1100 | 1200 | 1200 | 1200 | 1300 | 1600 | 1900 | 2300   | 2700   | 2700 | [outputs](outputs/baseline/2023-02-27)      |
| Gen2                  | GET  | /submitted/download-pdf | 2203          | 0             | 982.844529                | 353894.588              | 1.83656004 | 970  | 980  | 990  | 990  | 1000 | 1100 | 1200 | 1400 | 1700   | 2300   | 2300 | [outputs](outputs/investigation/2023-03-02) |

### Execution environment switch down-time
> As a part of this test, the benchmark was started on a fresh runner deployment on execution environment gen1. 
  > Midway through benchmark execution, runner was deployed with the execution environment gen2 and the 
  > [output](outputs/investigation/down-time-investigation) suggests no issue/errors reported and the traffic was managed properly by Cloud Run. 

#### Results based on 99th percentile timings.

| Metric                            | Investigation (gen1 to gen2 switch down-time)                                                        |
|-----------------------------------|------------------------------------------------------------------------------------------------------|
| GETs                              | 418ms                                                                                                |
| POSTs                             | 207ms                                                                                                |
| Total Requests                    | 60,861                                                                                               |
| 99th percentile Max CPU Usage (%) | 30.0%                                                                                                |
| Total Failures                    | 0                                                                                                    |
| Error Percentage                  | 0.0%                                                                                                 |
| Results                           | [benchmark_results](outputs/investigation/down-time-investigation/Results_For_Latest_Benchmark.yaml) |
| Performance Graph                 | [result](outputs/investigation/down-time-investigation/performance_graph.png)                        |


## Investigation

Looking at the performance results from both the Cloud Run execution environments, we were unable to find a major 
performance gain moving from first generation to second generation. Although GCP suggests faster CPU performance for 
second generation, but it seems to have no major impact on the performance for PDFkit and the response time stays more
or less nearly same. The `Load Balancer Backend Latency` check alert suggests the NFRs latency threshold, 
currently is 0.7 seconds but with second generation execution environment the average response time for PDF generation 
recorded was roughly 1 second.

If we decide to move to second generation execution environment:
- The investigation proved that there won't be any down-time necessary and the requests can be handled seamlessly.
- The investigation suggested no compatibility or cost implications.
- The investigation suggested the migration to be straight forward. As we are using terraform for the deployment which 
will require template metadata annotation `"run.googleapis.com/execution-environment"` as `"gen2"`.


## Recommendations

Cloud Run second generation execution does provide a slight improvement to the overall application performance 
it doesn't provide a major improvement to the response time for PDF generation. Making use of second generation execution
environment may provide certain benefits in the long run as it does provide faster CPU, network performance and support 
to the network file system which may be helpful for future features.

As second generation does not give us an immediate performance boost, the migration to the second generation execution 
environment can't be considered as a high priority but can be considered for future proofing.