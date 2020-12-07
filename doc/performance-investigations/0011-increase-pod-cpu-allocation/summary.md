# Kubernetes Pod CPU Usage

A number of benchmark tests were carried out to investigate the CPU usage of kubernetes pods, and how this effects Questionnaire Runner.

# Summary

## CPU Allocation

Our nodes (which are 4 core virtual machines) allocate CPU cores as follows:

- Each node has 3,920 mCPU allocatable.
- On each node, there is _always_ a minimum of 203 mCPU requested by pods in the `kube-system` namespace, leaving 3,717 mCPU for other pods.
- 648 mCPU of cores are requested by kube-system pods once per cluster. These can be put on a single node, or split across nodes if there are available CPU cores.
- In our test environment, there are 3 nodes, but only two Runner pods. There is variability in how the Runner and `kube-system` pods are arranged across the nodes. The following arrangements were observed during testing:
  1. `kube-system` pods placed onto the node with no Runner pods.
  1. `kube-system` pods placed entirely on one of the nodes that a Runner pod was also placed on.
  1. `kube-system` pods split across the nodes.
     There did not seem to be a definitive pattern to which nodes the `kube-system` pods were placed on, and even within a deployment, k8s was observed to kill pods and restart them on other nodes.
- Runner pods request 3000 mCPU, which is a minimum rather than a fixed amount. This means only one runner pod can exist on a single node at a given time given our current allocation of 4 cores per node.

When the additional `kube-system` pods were placed on the same node as the runner pods, response times were around 200ms slower when under load. This is likely a result of less CPU being available.

## Limit vs Request

At the moment we do not specify a limit for runner pod cpu usage. Rather, we request 3000 mCPU as a minimum, and set no limit. There is no benefit to setting a CPU allocation limit on our Runner workloads while we continue to run a single runner instance per node. Future performance investigations will look at scaling the machine types to higher core counts; that work should also investigate the performance of single runner pods compared to multiple runner pods per node. Should additional Runner pods per node be used, a limit should then be set on Runner's CPU usage to guard against resource contention by the pods.

## Fluentd Performance

Fluentd pods were observed to be using around 450 mCPU when under sustained load. Their requested cpu time is only 100 mCPU. Metrics gathered during recent stress tests show similar levels of CPU resource usage. Unfortunately, it was not feasible to measure the impact disabling app logging has at the cluster level; all of the tests run with fluentd disabled had multiple `kube-system` pods on Runner nodes. It is likely that that the increase in CPU resource used by fluentd under high load has a negative impact on response times. It may be beneficial to look at fluentd performance tuning.

## Decision

1. Do not increase the runner CPU request.
1. Test environments should use 3 runner pods on 3 nodes rather than the 2 pods that are currently deployed.
1. Investigate the feasibility of tuning fluentd.
1. Investigate performance when using different machine types
