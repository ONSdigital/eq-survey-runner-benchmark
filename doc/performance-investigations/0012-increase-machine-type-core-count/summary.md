# Investigate Machine Type Architecture Performance

EQ Runner currently uses a machine type of `custom-4-4096` (4 vCPU cores, 4096MB of RAM). This investigation looked at the impact of using larger instances with more pods on the performance of the runner application.

## Benchmark profile

| Option                 | Value                        |
| ---------------------- | ---------------------------- |
| Requests file          | census_household_gb_eng.json |
| Run time               | 20m                          |
| User wait time minimum | 1                            |
| User wait time maximum | 2                            |
| Clients per core       | 16                           |
| Number of workers      | 7                            |
| Number of threads      | 7                            |

This test replicates the current settings for the daily test.

## Results

| Cores | Pods | Nodes | GET Average | POST Average | All Request Average | Total Requests |
| ----- | ---- | ----- | ----------- | ------------ | ------------------- | -------------- |
| 4     | 4    | 4     | 572         | 609          | 590                 | 403,890        |
| 8     | 4    | 2     | 542         | 579          | 560                 | 404,535        |
| 16    | 4    | 1     | 620         | 651          | 636                 | 379,246        |
| 16    | 5    | 1     | 579         | 610          | 594                 | 394,487        |

In addition, a test was run against a node provisioned using a C type machine. C type machines have better per-core clock speeds, making them ideal for single-threaded applications. These tests were run with 64 clients.

| Architecture | Cores | Pods | Nodes | GET Average | POST Average | All Request Average | Total Requests |
| ------------ | ----- | ---- | ----- | ----------- | ------------ | ------------------- | -------------- |
| Default      | 4     | 1    | 1     | 239         | 288          | 263                 | 128,808        |
| C Type       | 4     | 1    | 1     | 136         | 113          | 125                 | 139,227        |

## Observations

- There is no significant difference in performance when using machines with more cores.
- There is a significant performance gain when using C type machines.

## Decision

- Continue to run using the 4 core machines currently provisioned.
- If the number of nodes that are required becomes the limiting factor in horizontal scaling, then larger machine types could be utilised.
- Further investigation of C type machines should be carried out to determine whether the performance seen in the cursory test carried out here can still be seen at higher loads.
- A further test of larger machines should be carried out, using a single runner pod per node and scaling the number of Gunicorn workers and threads relative to the available cores.
