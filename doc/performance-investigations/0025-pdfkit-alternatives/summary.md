# Saving answers as PDF: PDFKit (wkhtmltopdf) vs xhtml2pdf vs Weasyprint

Important notes:

* This investigation aims to repeat the previous investigation
  in [Investigation 0021](../0021-pdfkit-vs-weasyprint/summary.md), but now uses the new 'happy path' benchmark journey
  which includes the `/download-pdf` end point, along with the latest updates of dependencies and Runner.
* The benchmarks are very much a 'worst case scenario' because the journey _always_ hits the `/download-pdf` endpoint.
  In reality, not all users will download the PDF, so the overall impact on performance may be less significant.
* For every test in this investigation, we are using the default Design System's `print.css` file as the base CSS for
  generating the PDFs - this is currently mounted with Runner images. The big caveat here is that both `xhtml2pdf` and
  `weasyprint` do not support all CSS features, so some tweaking of the CSS file is required to get a reasonable output,
  but will be looked at separately.

Runner's current PDF implementation uses `pdfkit`; this package is a wrapper around the `wkhtmltopdf` binary, which
converts HTML to PDF using the Webkit rendering engine. Both of these are now deprecated, and there are concerns about
the performance, maintainability and security of this approach in the long term.

This investigation looks at `weasyprint` and `xhtml2pdf` as alternatives to understand any performance benefit from
moving over.

# Run #1 (moderate load)

## Runner settings

| Setting       | Value                                                                                             |
|---------------|---------------------------------------------------------------------------------------------------|
| Concurrency   | 115                                                                                               |
| Max instances | 3                                                                                                 |
| Min instances | 3                                                                                                 |
| CPU           | 4                                                                                                 |
| Memory        | 4G                                                                                                |
| Draft PR      | [EQS-512-alternatives-to-pdfkit](https://github.com/ONSdigital/eq-questionnaire-runner/pull/1816) |

## Benchmark profile

| Option                 | Value                                                                                                                                       |  
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|  
| Requests file          | test_benchmark_business_happy_path.json / test_benchmark_business_happy_path_xhtml2pdf.json / test_benchmark_business_happy_path_weasy.json |  
| Run time               | 10m                                                                                                                                         |  
| User wait time minimum | 1                                                                                                                                           |  
| User wait time maximum | 2                                                                                                                                           |  
| Clients                | 50                                                                                                                                          |  
| Hatch rate             | 50                                                                                                                                          |  

## Results

| Environment                             | Requests per second | GETs (99th) (ms) | POSTs (99th) (ms) | PDF GETs (50th) (ms) | PDF GETs (90th) (ms) | PDF GETs (95th) (ms) | PDF GETs (99th) (ms) | PDF GETs (99.9th) (ms) | PDF GETs (100th) (ms) | 99th percentile Max CPU Usage (%) | Total Requests | Total Failures | Outputs                                              |  
|-----------------------------------------|---------------------|------------------|-------------------|----------------------|----------------------|----------------------|----------------------|------------------------|-----------------------|-----------------------------------|----------------|----------------|------------------------------------------------------|
| Baseline with pdfkit                    | 57.60               | 362              | 133               | 1600                 | 1900                 | 2500                 | 3600                 | 4100                   | 4100                  | 30                                | 34,445         | 0              | [outputs](outputs/baseline/2026-01-26T13:41:05)      |  
| xhtml2pdf with custom CSS file (Run 1)  | 58.60               | 305              | 126               | 500                  | 640                  | 760                  | 970                  | 990                    | 990                   | 22                                | 35,032         | 0              | [outputs](outputs/investigation/2026-01-28T16:12:30) |
| xhtml2pdf with custom CSS file (Run 2)  | 58.78               | 258              | 139               | 540                  | 730                  | 790                  | 1100                 | 1200                   | 1200                  | 23                                | 35,109         | 0              | [outputs](outputs/investigation/2026-01-29T07:44:30) |
| weasyprint with custom CSS file (Run 1) | 58.20               | 291              | 139               | 1400                 | 2200                 | 2700                 | 3300                 | 3600                   | 3600                  | 29                                | 34,797         | 0              | [outputs](outputs/investigation/2026-01-29T11:10:19) |
| weasyprint with custom CSS file (Run 2) | 58.42               | 276              | 133               | 1200                 | 1800                 | 2000                 | 2800                 | 2900                   | 2900                  | 29                                | 34,918         | 0              | [outputs](outputs/investigation/2026-01-29T11:21:30) |

Observations:

* pdfkit performed consistently worse here
* weasyprint performed much better here than in the previous spike using the same custom CSS file to get a reasonable
  output. Median PDF GET response times were ~1200-1400ms, with 99th percentile times of ~2800-3300ms. CPU usage was
  similar to pdfkit at ~29% at 99th percentile.
* xhtml2pdf was the fastest option here, with median PDF GET response times of ~500-540ms, and 99th percentile times
  of ~970-1100ms. However, this is using a basic, stripped-down CSS file to get a reasonable output.

# Run #2 (heavy load)

## Runner settings

| Setting       | Value                                                                                             |
|---------------|---------------------------------------------------------------------------------------------------|
| Concurrency   | 115                                                                                               |
| Max instances | 50                                                                                                |
| Min instances | 3                                                                                                 |
| CPU           | 4                                                                                                 |
| Memory        | 4G                                                                                                |
| Draft PR      | [EQS-512-alternatives-to-pdfkit](https://github.com/ONSdigital/eq-questionnaire-runner/pull/1816) |

## Benchmark profile

| Option                 | Value                                                                                                                                       |  
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|  
| Requests file          | test_benchmark_business_happy_path.json / test_benchmark_business_happy_path_xhtml2pdf.json / test_benchmark_business_happy_path_weasy.json |  
| Run time               | 20m                                                                                                                                         |  
| User wait time minimum | 1                                                                                                                                           |  
| User wait time maximum | 2                                                                                                                                           |  
| Clients                | 200                                                                                                                                         |  
| Hatch rate             | 200                                                                                                                                         |  

## Results

| Environment                             | Requests per second | GETs (99th) (ms) | POSTs (99th) (ms) | PDF GETs (50th) (ms) | PDF GETs (90th) (ms) | PDF GETs (95th) (ms) | PDF GETs (99th) (ms) | PDF GETs (99.9th) (ms) | PDF GETs (100th) (ms) | 99th percentile Max CPU Usage (%) | Total Requests | Total Failures | Outputs                                              |  
|-----------------------------------------|---------------------|------------------|-------------------|----------------------|----------------------|----------------------|----------------------|------------------------|-----------------------|-----------------------------------|----------------|----------------|------------------------------------------------------|
| Baseline with pdfkit                    | 199.63              | 1958             | 973               | 2300                 | 7900                 | 11000                | 13000                | 16000                  | 16000                 | 71                                | 239,134        | 0              | [outputs](outputs/baseline/2026-01-30T11:47:22)      |  
| xhtml2pdf with custom CSS file (Run 1)  | 206.45              | 2988             | 581               | 770                  | 1400                 | 1700                 | 2200                 | 2900                   | 3300                  | 80                                | 247,165        | 0              | [outputs](outputs/investigation/2026-01-30T12:53:37) |
| xhtml2pdf with custom CSS file (Run 2)  | 206.27              | 1120             | 571               | 1100                 | 2100                 | 2600                 | 3700                 | 4600                   | 5300                  | 82                                | 247,000        | 0              | [outputs](outputs/investigation/2026-02-03T09:01:19) |
| weasyprint with custom CSS file (Run 1) | 202.44              | 1665             | 750               | 2000                 | 5600                 | 7700                 | 15000                | 19000                  | 19000                 | 87                                | 242,855        | 0              | [outputs](outputs/investigation/2026-01-30T13:27:52) |
| weasyprint with custom CSS file (Run 2) | 199.99              | 2061             | 1036              | 2400                 | 6300                 | 11000                | 18000                | 20000                  | 20000                 | 83                                | 239,427        | 0              | [outputs](outputs/investigation/2026-02-03T11:47:45) |

Observations:

* None of these packages performed particularly well under heavy load, with `weasyprint` showing the highest response
  times and CPU usage. However, it's worth noting that Runner's autoscaling did help to mitigate some of the performance
  issues by spinning up more instances to handle the load.
* Our current implementation with `pdfkit` peaked at 71% p99th CPU but then leveled off as Runner spun up more instances
  to handle the load, and generally hovered under ~60% CPU. This was a similar story with the other two packages, except
  that CPU hovered consistently above 60%
* `xhtml2pdf` is the fastest, but the speed came partly from a stripped CSS. This means no accessibility features, which
  is a big consideration for us.
* `weasyprint` gets us better CSS than `xhtml2pdf`, but heavy load shows CPU pressure (83–87% at p99), risking overall
  app latency. The Runner instance created more containers to handle the load, however.
* at 99%ile for PDF GETs, `weasyprint` crept up and overtook `pdfkit` with higher response times (15000ms) compared to
  `pdfkit` (13000ms)
* Errors with all packages were encountered during testing here in other runs (that I did not capture & document to
  prevent tainting these results). A separate ticket will be raised to look into these, as it could be caused by a
  myriad of factors unrelated to the PDF generation itself.

# Conclusion and recommendations

## Option 1: Do nothing

### Advantages

* This is the safest option, as `pdfkit` is currently ticking along okay within a 'reasonable' response time, although
  there are currently no NFRs for response times (as far as I know) so it's hard to say what is acceptable.
* We have an established implementation
* No development effort required & less risk of introducing new bugs

### Considerations

* This does not address the long-term concerns around maintainability and security - our Dockerfile now has several
  critical vulnerabilities due to the outdated `wkhtmltopdf` binary.
* Performance is not great, especially under load, and may degrade further with future updates to Runner.

## Option 2: Move to weasyprint

### Advantages

* `weasyprint` produces a reasonable output and has better support for modern CSS features than `xhtml2pdf`
* There appears to be a notable performance improvement using `weasyprint` since the original Spike
  `0018-pdf-weasyprint-pdfkit`. This is possibly due to improvements in the weasyprint library itself and makes use of
  newer features in the latest version of the library.

### Considerations:

* The big consideration here is the increased CPU usage compared to the other packages, which could impact overall
  application performance under load.
* We would need to ensure that the CSS file used for PDF generation is kept in sync with the main CSS file, which adds
  maintenance overhead.
* We would need to monitor CPU usage closely to ensure it does not degrade the user experience. Either way, this is a
  risky move, even now.
* Needs quite a few CSS tweaks to get it working like it is with Runner currently. For example, the current `print.css`
  file uses media queries, which
  `weasyprint` [does not currently support](https://github.com/Kozea/WeasyPrint/issues/494). Therefore, we would need to
  either liaise with DS to tweak their CSS, or maintain our own custom CSS file specifically for PDF generation, which
  would need to be kept in sync with any changes.
* Needs another benchmark with the updated code and CSS - this to make sure roughly the same outcome as benchmark from
  this spike. We might need to adjust NFRs accordingly in addition to this. We also might need to tweak the Runner
  settings for Cloud Run to higher CPU instances or lower max concurrency to account for the extra CPU usage
* Adds additional binaries to the Docker image, increasing the overall size, but possibly not much of a concern.
* Will need log suppression in Runner - there is a lot of event logging from the `weasyprint` library that clutters up
  the logs currently

## Option 3: Move to xhtml2pdf

### Advantages:

* By far the best performance of the three options tested here
* `xhtml2pdf` is more lightweight than `weasyprint`, resulting in lower CPU usage and potentially better overall
  application performance under load.

### Considerations:

* This is a big one - it is not as CSS-compliant as `weasyprint`, and has limited support for modern CSS features - it
  uses a small subset of CSS.
* Significant CSS tweaks are required to get a reasonable output to our `print.css` file, due to the limited CSS support
  in `xhtml2pdf`. This would require maintaining a custom CSS file specifically for PDF generation, as I don't think
  this would meet accessibility standards otherwise. Which leads me on to the next point...
* Accessibility is critical for respondents and government digital standards. We would need to spend time assessing
  whether the PDFs generated by `xhtml2pdf` meet these standards and what changes would be required to achieve this.
  This could add significant development and maintenance overhead.
* We would need to monitor CPU usage closely to ensure it does not degrade the user experience. Either way, this is a
  risky move, even now.
* Will need log suppression in Runner - there is a lot of event logging from the `xhtml2pdf` library that clutters up
  the logs currently

## Option 4: Explore other alternatives

* Other packages such as Playwright or headless Chrome in Python directly
* A headless browser approach might be a good replacement for `wkhtmltopdf` for security, even if it’s not the absolute
  fastest?

## Option 5: Create PDFs from scratch

* This would involve using a library such as ReportLab to create the PDFs programmatically, rather than converting from
  HTML. This would give us complete control over the PDF generation process and potentially better performance, but
  would require significant development effort to implement and maintain. This could be explored in a separate spike?

## Option 6: Use a separate PDF generation service

* This has been mentioned before (from previous spike) - it would involve using a third-party service like Playwright to
  handle PDF generation only, which could offload the processing from our Runner instances. However, this would
  introduce additional complexity and potential costs, as well as concerns around data privacy and security

## Option 7: Use a button or mouse wait loop icon while PDF is being generated

* This has been mentioned before (from previous spike) - maybe we could add a mouse cursor wait loop icon, or have a
  spinner on the button while the PDF is being generated to improve UX?
* This would need DS and accessibility considerations, but could be a low-effort way to improve the UX while we explore
  other options?

# Next steps

* Given the vulnerabilities in the current `wkhtmltopdf` binary, it may be worth considering moving away from `pdfkit`
  regardless of performance considerations. I think it might be worth exploring options 2, 4 and 7 in parallel to get a
  better understanding of the trade-offs between them, and to see if there are any other viable alternatives that we
  haven't considered yet.
* As a team, we will need to consider what is 'acceptable' performance for PDF generation in Runner, and whether the
  improvements seen with `weasyprint` or `xhtml2pdf` justify the potential downsides
* We will need to decide on the best approach based on the downsides outlined above, considering factors such as
  performance, maintainability, security, and accessibility.
