#

## prometheus operator

> https://github.com/coreos/prometheus-operator
> https://www.kancloud.cn/huyipow/prometheus/529066

## kube-prometheus

> https://github.com/coreos/kube-prometheus

## kops cluster_spec

> https://github.com/kubernetes/kops/blob/master/docs/cluster_spec.md#hooks

## kops metrics-server

> https://github.com/kubernetes/kops/tree/master/addons/metrics-server

## kops prometheus operator addon

> https://github.com/kubernetes/kops/tree/master/addons/prometheus-operator

## access dashboard

* Prometheus

  * `kubectl --namespace monitoring port-forward svc/prometheus-k8s 9090`

  * access via http://localhost:9090

  * kubelet broken pipe issue...

    ```bash
    Handling connection for 9090
    E0517 15:49:53.307797    8155 portforward.go:372] error copying from remote stream to local connection: readfrom tcp6 [::1]:9090->[::1]:46214: write tcp6 [::1]:9090->[::1]:46214: write: broken pipe
    E0517 15:50:00.194578    8155 portforward.go:340] error creating error stream for port 9090 -> 9090: Timeout occured
    Handling connection for 9090
    E0517 15:50:00.195119    8155 portforward.go:340] error creating error stream for port 9090 -> 9090: Timeout occured
    Handling connection for 9090
    E0517 15:50:13.142690    8155 portforward.go:340] error creating error stream for port 9090 -> 9090: Timeout occured
    E0517 15:50:23.917633    8155 portforward.go:362] error creating forwarding stream for port 9090 -> 9090: Timeout occured
    E0517 15:50:30.195092    8155 portforward.go:340] error creating error stream for port 9090 -> 9090: Timeout occured
    E0517 15:50:30.196019    8155 portforward.go:340] error creating error stream for port 9090 -> 9090: Timeout occured
    ```

    https://github.com/kubernetes/kubernetes/issues/74551

    **wait for about 1 min, this error disappeared...**
    i think it's a network connection problem...

* Grafana
  * `kubectl --namespace monitoring port-forward svc/grafana 3000`
  * access via http://localhost:3000
  * **default grafana user:password of admin:admin**

* Alert Manager
  * `kubectl --namespace monitoring port-forward svc/alertmanager-main 9093`
  * access via http://localhost:9093
  * alert manager `CrashLoopBackOff`

    ```bash
    ➜  Rook git:(master) ✗ kubectl describe -n monitoring pods/alertmanager-main-0
    Name:               alertmanager-main-0
    Namespace:          monitoring
    Priority:           0
    PriorityClassName:  <none>
    Node:               ip-172-20-35-247.ec2.internal/172.20.35.247
    Start Time:         Fri, 17 May 2019 15:43:01 +0800
    Labels:             alertmanager=main
                        app=alertmanager
                        controller-revision-hash=alertmanager-main-77d58f899d
                        statefulset.kubernetes.io/pod-name=alertmanager-main-0
    Annotations:        <none>
    Status:             Running
    IP:                 100.96.1.10
    Controlled By:      StatefulSet/alertmanager-main
    Containers:
    alertmanager:
        Container ID:  docker://3680910adefcaccb04ef15f6556f43de7726de52ff358803f529f2a5b1e01b90
        Image:         quay.io/prometheus/alertmanager:v0.15.3
        Image ID:      docker-pullable://quay.io/prometheus/alertmanager@sha256:27410e5c88aaaf796045e825b257a0857cca0876ca3804ba61175dd8a9f5b798
        Ports:         9093/TCP, 6783/TCP
        Host Ports:    0/TCP, 0/TCP
        Args:
        --config.file=/etc/alertmanager/config/alertmanager.yaml
        --cluster.listen-address=[$(POD_IP)]:6783
        --storage.path=/alertmanager
        --data.retention=120h
        --web.listen-address=:9093
        --web.route-prefix=/
        --cluster.peer=alertmanager-main-0.alertmanager-operated.monitoring.svc:6783
        --cluster.peer=alertmanager-main-1.alertmanager-operated.monitoring.svc:6783
        --cluster.peer=alertmanager-main-2.alertmanager-operated.monitoring.svc:6783
        State:          Running
        Started:      Fri, 17 May 2019 15:43:04 +0800
        Ready:          True
        Restart Count:  0
        Requests:
        memory:   200Mi
        Liveness:   http-get http://:web/api/v1/status delay=0s timeout=3s period=10s #success=1 #failure=10
        Readiness:  http-get http://:web/api/v1/status delay=3s timeout=3s period=5s #success=1 #failure=10
        Environment:
        POD_IP:   (v1:status.podIP)
        Mounts:
        /alertmanager from alertmanager-main-db (rw)
        /etc/alertmanager/config from config-volume (rw)
        /var/run/secrets/kubernetes.io/serviceaccount from alertmanager-main-token-cl9pn (ro)
    config-reloader:
        Container ID:  docker://2c5cd25f9288a2106ce17becf1612cb111afcb639243cc4e4cf511952d85802d
        Image:         quay.io/coreos/configmap-reload:v0.0.1
        Image ID:      docker-pullable://quay.io/coreos/configmap-reload@sha256:e2fd60ff0ae4500a75b80ebaa30e0e7deba9ad107833e8ca53f0047c42c5a057
        Port:          <none>
        Host Port:     <none>
        Args:
        -webhook-url=http://localhost:9093/-/reload
        -volume-dir=/etc/alertmanager/config
        State:          Waiting
        Reason:       CrashLoopBackOff
        Last State:     Terminated
        Reason:       ContainerCannotRun
        Message:      OCI runtime create failed: container_linux.go:348: starting container process caused "process_linux.go:402: container init caused \"process_linux.go:367: setting cgroup config for procHooks process caused \\\"failed to write 10485760 to memory.limit_in_bytes: write /sys/fs/cgroup/memory/kubepods/burstable/pod6601d27f-7877-11e9-a3e2-0a96c25a44aa/2c5cd25f9288a2106ce17becf1612cb111afcb639243cc4e4cf511952d85802d/memory.limit_in_bytes: device or resource busy\\\"\"": unknown
        Exit Code:    128
        Started:      Fri, 17 May 2019 16:34:55 +0800
        Finished:     Fri, 17 May 2019 16:34:55 +0800
        Ready:          False
        Restart Count:  15
        Limits:
        cpu:     5m
        memory:  10Mi
        Requests:
        cpu:        5m
        memory:     10Mi
        Environment:  <none>
        Mounts:
        /etc/alertmanager/config from config-volume (ro)
        /var/run/secrets/kubernetes.io/serviceaccount from alertmanager-main-token-cl9pn (ro)
    Conditions:
    Type              Status
    Initialized       True 
    Ready             False 
    ContainersReady   False 
    PodScheduled      True 
    Volumes:
    config-volume:
        Type:        Secret (a volume populated by a Secret)
        SecretName:  alertmanager-main
        Optional:    false
    alertmanager-main-db:
        Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
        Medium:     
        SizeLimit:  <unset>
    alertmanager-main-token-cl9pn:
        Type:        Secret (a volume populated by a Secret)
        SecretName:  alertmanager-main-token-cl9pn
        Optional:    false
    QoS Class:       Burstable
    Node-Selectors:  beta.kubernetes.io/os=linux
    Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                    node.kubernetes.io/unreachable:NoExecute for 300s
    Events:
    Type     Reason     Age                   From                                    Message
    ----     ------     ----                  ----                                    -------
    Normal   Scheduled  54m                   default-scheduler                       Successfully assigned monitoring/alertmanager-main-0 to ip-172-20-35-247.ec2.internal
    Normal   Pulling    54m                   kubelet, ip-172-20-35-247.ec2.internal  pulling image "quay.io/prometheus/alertmanager:v0.15.3"
    Normal   Pulled     54m                   kubelet, ip-172-20-35-247.ec2.internal  Successfully pulled image "quay.io/prometheus/alertmanager:v0.15.3"
    Normal   Created    54m                   kubelet, ip-172-20-35-247.ec2.internal  Created container
    Normal   Started    54m                   kubelet, ip-172-20-35-247.ec2.internal  Started container
    Normal   Pulling    54m                   kubelet, ip-172-20-35-247.ec2.internal  pulling image "quay.io/coreos/configmap-reload:v0.0.1"
    Normal   Pulled     54m                   kubelet, ip-172-20-35-247.ec2.internal  Successfully pulled image "quay.io/coreos/configmap-reload:v0.0.1"
    Normal   Created    52m (x5 over 54m)     kubelet, ip-172-20-35-247.ec2.internal  Created container
    Warning  Failed     52m (x5 over 54m)     kubelet, ip-172-20-35-247.ec2.internal  Error: failed to start container "config-reloader": Error response from daemon: OCI runtime create failed: container_linux.go:348: starting container process caused "process_linux.go:402: container init caused \"process_linux.go:367: setting cgroup config for procHooks process caused \\\"failed to write 10485760 to memory.limit_in_bytes: write /sys/fs/cgroup/memory/kubepods/burstable/pod6601d27f-7877-11e9-a3e2-0a96c25a44aa/config-reloader/memory.limit_in_bytes: device or resource busy\\\"\"": unknown
    Normal   Pulled     52m (x4 over 54m)     kubelet, ip-172-20-35-247.ec2.internal  Container image "quay.io/coreos/configmap-reload:v0.0.1" already present on machine
    Warning  BackOff    4m8s (x224 over 53m)  kubelet, ip-172-20-35-247.ec2.internal  Back-off restarting failed container
    ```

  * similar to this issue: https://github.com/coreos/prometheus-operator/issues/2364
  * need update prometheus-operator version
  * execute `addon/gen.sh`
  * `kubectl apply -f /home/harold/Desktop/Notes/cloud/Prometheus/addon/v0.30.0.yaml`
  * now all pods work well!