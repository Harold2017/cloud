#

## grafana dashboard displays wrong cpu cores and memory usage

### check on prometheus

use the following query:

```bash
node:node_num_cpu:sum
machine_cpu_cores
```

[query link](http://localhost:3000/graph?g0.range_input=1h&g0.expr=node%3Anode_num_cpu%3Asum&g0.tab=1&g1.range_input=1h&g1.expr=%3Akube_pod_info_node_count%3A&g1.tab=1&g2.range_input=1h&g2.expr=node%3Anode_memory_utilisation%3Aratio&g2.tab=1&g3.range_input=1h&g3.expr=%3Anode_memory_MemTotal_bytes%3Asum&g3.tab=1&g4.range_input=1h&g4.expr=node%3Anode_memory_bytes_total%3Asum&g4.tab=1&g5.range_input=1h&g5.expr=machine_cpu_cores&g5.tab=1&g6.range_input=1h&g6.expr=%3Anode_memory_MemFreeCachedBuffers_bytes%3Asum&g6.tab=1&g7.range_input=1h&g7.expr=machine_memory_bytes&g7.tab=1&g8.range_input=1h&g8.expr=namespace%3Acontainer_memory_usage_bytes%3Asum&g8.tab=1&g9.range_input=1h&g9.expr=sum(process_virtual_memory_bytes)&g9.tab=1&g10.range_input=1h&g10.expr=process_virtual_memory_max_bytes&g10.tab=1&g11.range_input=1h&g11.expr=sum(process_resident_memory_bytes)&g11.tab=1)

find `machine_cpu_cores` is 32 >> node_num_cpu:sum (8)

|Element|Value|
|--- |--- |
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.148:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-148",service="kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.148:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-148",service="monitor-prometheus-operato-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.148:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-148",service="monitor-release-prometheus-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.148:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-148",service="test-release-prometheus-op-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.58:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-58",service="kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.58:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-58",service="monitor-prometheus-operato-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.58:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-58",service="monitor-release-prometheus-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.58:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-58",service="test-release-prometheus-op-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.69:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-69",service="kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.69:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-69",service="monitor-prometheus-operato-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.69:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-69",service="monitor-release-prometheus-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.69:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-69",service="test-release-prometheus-op-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.79:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-79",service="kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.79:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-79",service="monitor-prometheus-operato-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.79:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-79",service="monitor-release-prometheus-kubelet"}|2|
|machine_cpu_cores{endpoint="https-metrics",instance="10.0.2.79:10250",job="kubelet",namespace="kube-system",node="ip-10-0-2-79",service="test-release-prometheus-op-kubelet"}|2|

note that some kubelet services should have been deleted... (`test-release*`, `monitor-release*`)

need manually delete them

```bash
➜  cloud git:(master) ✗ kubectl delete service test-release-prometheus-op-kubelet -n kube-system
service "test-release-prometheus-op-kubelet" deleted
➜  cloud git:(master) ✗ kubectl delete service monitor-release-prometheus-kubelet -n kube-system
service "monitor-release-prometheus-kubelet" deleted
```

**then the cpu cores are normal now**

memory usage on grafana dashboard is virtual memory

resident memory usage is low

it can be checked through prometheus (former link) or through `top` on pods
