# Saving answer as PDF: Weasyprint vs PDFKit (wkhtmltopdf)

Runner’s current PDF implementation uses PDFKit; this investigation looks at Weasyprint as an alternative to understand any performance benefit from moving over.

**Notes:**
- Caveat on speed from the docs of weasyprint: `WeasyPrint is often slower than other web engines. Python is the usual suspect, but it’s not the main culprit here. Optimization is not the main goal of WeasyPrint, and it may lead to unbearable long rendering times.`
- V2 is faster not because of the library per se but because it has far fewer CSS rules to evaluate. v2 has ~9k+ of CSS, whereas v3 has ~40k+ lines of CSS, slowing down the rendering.
- To get weasyprint working with v3 required having a custom CSS file which removed a lot of the CSS, especially the ones that Weasyprint does not support, such as media queries. Supported features of CSS: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html#css
- The POC delivered a reasonable-looking PDF in Weasyprint for demonstration purposes; the CSS still needs tweaks. To take this approach, we need to understand how the CSS file will be managed and who will manage it.
- In local dev envs (on Mac), weasyprint is much faster ~x3; however, on Docker, weasyprint is only slightly faster by not that much but enough to be within the NFRs of ~2 the second load. This could be because the current package is inconsistent, as sometimes is it fast, sometimes slow. We need to ensure weasyprint is consistent under the ~2-second mark.    
  The POC delivered is mostly 1-2 seconds. WKHTML seems to only be slow on the initial download request as it might be doing some caching or the library binaries don’t need reloading, so subsequent download appears to be faster. This may even apply between instances/users. In my testing, WKHTML was only sometimes slow. In most cases, it was on par with weasyprint.

This documentation benchmarks Weasyprint and PDFKit under higher loads to see the performance differences and whether the libraries take advantage of some caching.

## Runner settings

| Setting       | Value                                                                                                                                             |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Concurrency   | 115                                                                                                                                               |
| Max instances | 3                                                                                                                                                 |
| Min instances | 3                                                                                                                                                 |
| CPU           | 4                                                                                                                                                 |
| Memory        | 4G                                                                                                                                                |
| Commit        | [4e810eb782d0614563a13844def69dd42b1770b3](https://github.com/ONSdigital/eq-questionnaire-runner/commit/4e810eb782d0614563a13844def69dd42b1770b3) |

When testing PDFKit with a custom CSS file, commit [03f3bccbd37e4f31d9621137dc8ba12ce5dc3b0b](https://github.com/ONSdigital/eq-questionnaire-runner/commit/03f3bccbd37e4f31d9621137dc8ba12ce5dc3b0b)  was used, which implemented this. This should have no impact on the other test runs.

## Benchmark profile

| Option                 | Value                                                                                                   |  
|------------------------|---------------------------------------------------------------------------------------------------------|  
| Requests file          | test_business_benchmark.json / test_business_benchmark_weasy.json / test_business_benchmark_pdfkit.json |  
| Run time               | 10m                                                                                                     |  
| User wait time minimum | 1                                                                                                       |  
| User wait time maximum | 2                                                                                                       |  
| Clients                | 50                                                                                                      |  
| Hatch rate             | 50                                                                                                      |  

## Results

| Environment                                              | Requests per second | GETs (99th) (ms) | POSTs (99th) (ms) | PDF GETs (50th) (ms) | PDF GETs (90th) (ms) | PDF GETs (95th) (ms) | PDF GETs (99th) (ms) | PDF GETs (99.9th) (ms) | PDF GETs (100th) (ms) | 99th percentile Max CPU Usage (%) | Total Requests | Total Failures | Outputs                                              |  
|----------------------------------------------------------|---------------------|------------------|-------------------|----------------------|----------------------|----------------------|----------------------|------------------------|-----------------------|-----------------------------------|----------------|----------------|------------------------------------------------------|  
| Baseline fresh deployment (No PDF download requested)    | 55.41               | 334              | 107               | N/A                  | N/A                  | N/A                  | N/A                  | N/A                    | N/A                   | 14.9                              | 33,246         | 0              | [outputs](outputs/baseline/2022-02-17T14:49:13)      |  
| Weasyprint with custom CSS file(Run 1, fresh deployment) | 50.91               | 769              | 143               | 1300                 | 2100                 | 2700                 | 7400                 | 9200                   | 10000                 | 38                                | 30,548         | 0              | [outputs](outputs/investigation/2022-02-17T15:17:20) |  
| Weasyprint with custom CSS file (Run 2)                  | 51.33               | 415              | 142               | 1300                 | 2200                 | 2900                 | 4400                 | 6200                   | 7100                  | 36                                | 30,803         | 0              | [outputs](outputs/investigation/2022-02-17T15:30:33) |  
| PDFKit existing implementation (Run 1, fresh deployment) | 51.64               | 496              | 126               | 1200                 | 1400                 | 1700                 | 2400                 | 3300                   | 3600                  | 30.9                              | 30,988         | 0              | [outputs](outputs/investigation/2022-02-17T15:50:06) |  
| PDFKit existing implementation (Run 2)                   | 52                  | 311              | 125               | 1200                 | 1400                 | 1600                 | 2600                 | 3100                   | 3100                  | 32                                | 31,200         | 1              | [outputs](outputs/investigation/2022-02-17T16:03:39) |  
| PDFKit with custom CSS file (Run 1, fresh deployment)    | 51.49               | 558              | 191               | 1100                 | 1300                 | 1400                 | 2300                 | 2900                   | 3200                  | 30.9                              | 30,896         | 0              | [outputs](outputs/investigation/2022-02-18T11:43:31) |  
| PDFKit with custom CSS file (Run 2)                      | 51.60               | 308              | 141               | 1100                 | 1300                 | 1300                 | 2200                 | 2600                   | 2600                  | 30                                | 30,961         | 0              | [outputs](outputs/investigation/2022-02-18T11:57:06) |  

Error for PDFKit (Run 2):
- 1 x Expected a (302) but got a (0) back when posting page: /questionnaire/introduction-block/. No corresponding error found in runner.

### Cloud Run 2nd Generation Execution Environment

From GCP docs:

```  
By default, Cloud Run services operate within the first generation execution environment, which features fast cold start times and emulation of most, but not all operating system calls. Originally, this was the only execution environment available to services in Cloud Run.   
    
The second-generation execution environment provides full Linux compatibility rather than system call emulation. This execution environment provides:   
    
- Faster CPU performance   
- Faster network performance, especially in the presence of packet loss   
- Full Linux compatibility, including support for all system calls, namespaces, and cgroups   
- Network file system support   
```  

The following results are benchmarked against runner using Cloud Run’s second-generation execution environments. These are not fresh deployments, a 1 -minute warm-up test was run.

| Environment                          | Requests per second | GETs (99th) (ms) | POSTs (99th) (ms) | PDF GETs (50th) (ms) | PDF GETs (90th) (ms) | PDF GETs (95th) (ms) | PDF GETs (99th) (ms) | PDF GETs (99.9th) (ms) | PDF GETs (100th) (ms) | 99th percentile Max CPU Usage (%) | Total Requests | Total Failures | Outputs                                                                     |  
|--------------------------------------|---------------------|------------------|-------------------|----------------------|----------------------|----------------------|----------------------|------------------------|-----------------------|-----------------------------------|----------------|----------------|-----------------------------------------------------------------------------|  
| Baseline (No PDF download requested) | 55.79               | 160              | 104               | N/A                  | N/A                  | N/A                  | N/A                  | N/A                    | N/A                   | 12                                | 33,477         | 0              | [outputs](outputs/baseline/2022-02-17T16:30:36-Gen2)                        |  
| Weasyprint with custom CSS file      | 51.84               | 482              | 126               | 1100                 | 1600                 | 2000                 | 5800                 | 6800                   | 7200                  | 35                                | 31,105         | 0              | [outputs](outputs/investigation/2022-02-17T16:46:37-weasyprint-gen-2)       |  
| PDFKit existing implementation       | 52.43               | 231              | 108               | 950                  | 1100                 | 1200                 | 1500                 | 2100                   | 2200                  | 26                                | 31,458         | 0              | [outputs](outputs/investigation/2022-02-17T16:59:03-pdfkit-gen-2)           |  
| PDFKit with custom CSS file          | 52.92               | 221              | 112               | 820                  | 970                  | 1000                 | 1100                 | 1400                   | 1400                  | 23.9                              | 31,752         | 17  (0.05%)    | [outputs](outputs/investigation/2022-02-18T13:09:33-pdfkit-optimised-gen-2) |  

Error for PDFKit with custom CSS file:
- 17 x 500 `ConnectionResetError`  on runner during submission due to some issue with GCS.  GCP status reported no GCS incidents at the time.

```  
"  File '/usr/local/lib/python3.9/site-packages/google/resumable_media/requests/upload.py', line 145, in retriable_request"  
88: "    result = transport.request("  
89: "  File '/usr/local/lib/python3.9/site-packages/google/auth/transport/requests.py', line 480, in request"  
90: "    response = super(AuthorizedSession, self).request("  
91: "  File '/usr/local/lib/python3.9/site-packages/requests/sessions.py', line 529, in request"  
92: "    resp = self.send(prep, **send_kwargs)"  
93: "  File '/usr/local/lib/python3.9/site-packages/requests/sessions.py', line 645, in send"  
94: "    r = adapter.send(request, **kwargs)"  
95: "  File '/usr/local/lib/python3.9/site-packages/requests/adapters.py', line 501, in send"  
96: "    raise ConnectionError(err, request=request)"  
97: "requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))"  
```  


## Findings

- The response time tends to be slightly higher after a new deployment.
- Weasyprint is significantly more CPU intensive than PDFKit resulting in the degradation of the entire app. To use Weasyprint, we require custom CSS files and nodes with a higher CPU count or lower max concurrency to account for the extra CPU usage.
- PDFKit’s response times improve after the initial deployment. Therefore, we should expect spikes in the PDF response times after a deployment.
- PDFKit’s performance improved when using a smaller custom CSS file.
- Using the second-generation Cloud Run execution environment resulted in some performance improvements to the whole application. More importantly, this environment makes the response times for PDFKit much more performant and closer to the NFRs. This implies that the speed gain is from the `wkhtmltopdf` executable instead of caching.
- Runner can support fewer requests per second when considering the PDF journey, which results in almost twice the CPU usage than without the PDF journey.

## Next steps

- Use PDFKit with the existing implementation unless the above conditions are not acceptable. Consider whether it becomes acceptable if we were using a custom CSS file or the 2nd Gen Cloud Run execution environment, or both. If not acceptable:
  - Investigate:
    - creating the PDF from scratch (not from HTML)
    - using another PDF library / 3rd party service.
    - preloading the PDF
- If possible, move to Second Generation Cloud Run execution environment once it is out of Beta.
- Re-understand runner’s maximum capability considering the CPU impact the PDF generation has on the node.
