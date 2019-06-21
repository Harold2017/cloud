#

## kontena pharos

> https://www.kontena.io/pharos

## get started

> https://pharos.sh/docs/getting-started

* setup kontena pharos cli toolchain
  * install chpharos - the pharos version switcher tool
  `curl -s https://get.pharos.sh | bash`
  * login
  `chpharos login`
  * install pharos cli tool binaries
  `chpharos install latest+oss --use`

* prepare nodes for k8s cluster
  * containers on linux distro

* create the cluster configuration file
  * yaml file

* bootstrap k8s cluster
  * in the same dir where cluster.yml file, run
  `pharos up -c cluster.yml` (--force if need update pharos) (add `-d` for debug info)
  * port config of node: https://github.com/kontena/pharos-docs/blob/master/networking/firewalld.md
  * watchout: if add nodes to the existed cluster, the new nodes should be in the same VPC (subnet) with cluster

* interact with the cluster
  * get kubeconfig file and run
  `pharos kubeconfig > kubeconfig`
  `export KUBECONFIG=./kubeconfig`

## [Ceph Operator Helm Chart](https://github.com/rook/rook/blob/master/Documentation/helm-operator.md)

```bash
# Create a ServiceAccount for Tiller in the `kube-system` namespace
kubectl --namespace kube-system create sa tiller

# Create a ClusterRoleBinding for Tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller

# Patch Tiller's Deployment to use the new ServiceAccount
kubectl --namespace kube-system patch deploy/tiller-deploy -p '{"spec": {"template": {"spec": {"serviceAccountName": "tiller"}}}}'

# Install
helm repo add rook-release https://charts.rook.io/release
helm install --namespace rook-ceph rook-release/rook-ceph

# Cluster
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/example_yaml/cluster_default.yaml 
cephcluster.ceph.rook.io/rook-ceph created

# Toolbox
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/example_yaml/toolbox.yaml 
deployment.apps/rook-ceph-tools created

# Check cluster pods
➜  cloud git:(master) ✗ kubectl get pods
NAME                                        READY   STATUS      RESTARTS   AGE
rook-ceph-agent-6tq8b                       1/1     Running     0          17m
rook-ceph-agent-bxw8h                       1/1     Running     0          17m
rook-ceph-agent-rlhwr                       1/1     Running     0          17m
rook-ceph-mgr-a-7ff96fc4b9-sfwt8            1/1     Running     0          5m6s
rook-ceph-mon-a-6cf57f85c-ld8q5             1/1     Running     0          6m25s
rook-ceph-mon-b-665bcb9f79-jplcb            1/1     Running     0          5m57s
rook-ceph-mon-c-654c5cd6dd-wrjrz            1/1     Running     0          5m28s
rook-ceph-operator-54476dc55f-ddpms         1/1     Running     0          17m
rook-ceph-osd-0-59586947bc-4z5zs            1/1     Running     0          4m31s
rook-ceph-osd-1-9f4bd8d9f-mv66m             1/1     Running     0          4m31s
rook-ceph-osd-2-5cb69b5bc6-lx776            1/1     Running     0          4m31s
rook-ceph-osd-prepare-ip-10-0-2-148-mb7gj   0/2     Completed   0          4m38s
rook-ceph-osd-prepare-ip-10-0-2-69-kjpk9    0/2     Completed   0          4m38s
rook-ceph-osd-prepare-ip-10-0-2-79-rj2t4    0/2     Completed   0          4m38s
rook-ceph-rgw-my-store-5b8c8bb954-zs6d4     1/1     Running     0          23s
rook-ceph-tools-7c4f75b579-j7vjq            1/1     Running     0          16s
rook-discover-m4d92                         1/1     Running     0          17m
rook-discover-t8vb6                         1/1     Running     0          17m
rook-discover-wcbv9                         1/1     Running     0          17m

# Create sc
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/example_yaml/storageclass2.yaml 
cephblockpool.ceph.rook.io/gppool created
storageclass.storage.k8s.io/rook-ceph-block-gp created

# Object storage
# create object store
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/example_yaml/object.
yaml 
cephobjectstore.ceph.rook.io/my-store created
# create rgw gateway
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/example_yaml/rgw-external.yaml 
service/rook-ceph-rgw-my-store-external created
➜  cloud git:(master) ✗ kubectl -n rook-ceph get service rook-ceph-rgw-my-store rook-ceph-rgw-my-store-external
NAME                              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
rook-ceph-rgw-my-store            ClusterIP   10.97.105.1    <none>        80/TCP         3m26s
NAME                              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
rook-ceph-rgw-my-store-external   NodePort    10.106.7.164   <none>        80:31586/TCP   86s
# create user
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/example_yaml/object-user.yaml
cephobjectstoreuser.ceph.rook.io/my-user created
# obtain user secret
➜  cloud git:(master) ✗ kubectl -n rook-ceph describe secret | grep my-store  
Name:         rook-ceph-object-user-my-store-my-user
              rook_object_store=my-store
Name:         rook-ceph-rgw-my-store-keyring
➜  cloud git:(master) ✗ kubectl -n rook-ceph describe secret rook-ceph-object-user-my-store-my-user
Name:         rook-ceph-object-user-my-store-my-user
Namespace:    rook-ceph
Labels:       app=rook-ceph-rgw
              rook_cluster=rook-ceph
              rook_object_store=my-store
              user=my-user
Annotations:  <none>

Type:  kubernetes.io/rook

Data
====
SecretKey:  40 bytes
AccessKey:  20 bytes
➜  cloud git:(master) ✗ kubectl -n rook-ceph get secret rook-ceph-object-user-my-store-my-user -o yaml | grep AccessKey | awk '{print $2}' | base64 --decode
<access-key>
➜  cloud git:(master) ✗ kubectl -n rook-ceph get secret rook-ceph-object-user-my-store-my-user -o yaml | grep SecretKey | awk '{print $2}' | base64 --decode
<secret-key>
# test with `s3test.py`
# test 1
➜  Rook git:(master) ✗ python3 s3test.py
my-new-bucket 2019-05-28T02:02:01.706Z
# test 2
➜  Rook git:(master) ✗ python3 s3test.py
[]
b'this is a test of s3 bucket object storage'
# test 3
➜  Rook git:(master) ✗ python3 s3test.py
time consumption:  0.5131204128265381
time consumption:  0.4713881015777588
[<Key: my-new-bucket,test>, <Key: my-new-bucket,test_jpg>]
# check on rook-ceph-toolbox
[root@ip-10-0-2-69 /]# ceph df
RAW STORAGE:
    CLASS     SIZE        AVAIL       USED       RAW USED     %RAW USED 
    ssd       436 GiB     407 GiB     29 GiB       29 GiB          6.70 
    TOTAL     436 GiB     407 GiB     29 GiB       29 GiB          6.70 
 
POOLS:
    POOL                           ID     STORED      OBJECTS     USED        %USED     MAX AVAIL 
    gppool                          1         0 B           0         0 B         0       128 GiB 
    my-store.rgw.control            2         0 B           8         0 B         0       128 GiB 
    .rgw.root                       3     3.8 KiB          16     3.8 KiB         0       385 GiB 
    my-store.rgw.meta               4       838 B           5       838 B         0       128 GiB 
    my-store.rgw.log                5        50 B         212        50 B         0       128 GiB 
    my-store.rgw.buckets.index      6         0 B           1         0 B         0       128 GiB 
    my-store.rgw.buckets.data       7      32 KiB           2      32 KiB         0       128 GiB 
# check pool
[root@ip-10-0-2-69 /]# ceph osd pool ls
gppool
my-store.rgw.control
.rgw.root
my-store.rgw.meta
my-store.rgw.log
my-store.rgw.buckets.index
my-store.rgw.buckets.data
# get full ceph cluster report
[root@ip-10-0-2-69 /]# ceph report
...
# investigate more cmd with ceph --help


# create a new namespace `monitoring` to install prometheus
➜  cloud git:(master) ✗ kubectl create -f namespace-monitoring.jsonnamespace/monitoring created
➜  cloud git:(master) ✗ kubectl get namespaces
NAME            STATUS   AGE
default         Active   16h
ingress-nginx   Active   16h
kube-public     Active   16h
kube-system     Active   16h
monitoring      Active   11s
rook-ceph       Active   16h
# install prometheus-operator
➜  cloud git:(master) ✗ helm install --name test-release stable/prometheus-operator --namespace monitoring
# check on `monitoring` namespace
➜  cloud git:(master) ✗ kubectl get pods 
NAME                                                     READY   STATUS    RESTARTS   AGE
alertmanager-test-release-prometheus-op-alertmanager-0   2/2     Running   0          42s
prometheus-test-release-prometheus-op-prometheus-0       3/3     Running   1          36s
test-release-grafana-84dd68976c-wdz45                    2/2     Running   0          49s
test-release-kube-state-metrics-74db479f9c-57k2n         1/1     Running   0          49s
test-release-prometheus-node-exporter-5lk8q              1/1     Running   0          49s
test-release-prometheus-node-exporter-8687g              1/1     Running   0          49s
test-release-prometheus-node-exporter-88794              1/1     Running   0          49s
test-release-prometheus-node-exporter-cddk6              1/1     Running   0          49s
test-release-prometheus-op-operator-69459864c5-9qxbf     1/1     Running   0          49s
# check svc
➜  cloud git:(master) ✗ kubectl get svc 
NAME                                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
alertmanager-operated                     ClusterIP   None            <none>        9093/TCP,6783/TCP   2m1s
prometheus-operated                       ClusterIP   None            <none>        9090/TCP            115s
test-release-grafana                      ClusterIP   10.109.31.138   <none>        80/TCP              2m9s
test-release-kube-state-metrics           ClusterIP   10.109.149.14   <none>        8080/TCP            2m9s
test-release-prometheus-node-exporter     ClusterIP   10.98.181.253   <none>        9100/TCP            2m9s
test-release-prometheus-op-alertmanager   ClusterIP   10.108.207.45   <none>        9093/TCP            2m9s
test-release-prometheus-op-operator       ClusterIP   10.106.232.25   <none>        8080/TCP            2m8s
test-release-prometheus-op-prometheus     ClusterIP   10.108.17.164   <none>        9090/TCP            2m8s
# grafana login credentials
User: admin
Password:
➜  cloud git:(master) ✗ kubectl get secret --namespace monitoring test-release-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
# forward the port to localhost to watch it
➜  cloud git:(master) ✗ kubectl --namespace monitoring port-forward svc/test-release-grafana 3000:80
Forwarding from 127.0.0.1:3000 -> 3000
Forwarding from [::1]:3000 -> 3000
# check on http://localhost:3000

# uninstall
helm delete test-release
helm del --purge test-release
# after delete the release, also need delete CRDs
# CRDs created by this chart are not removed by default and should be manually cleaned up
kubectl delete crd prometheuses.monitoring.coreos.com
kubectl delete crd prometheusrules.monitoring.coreos.com
kubectl delete crd servicemonitors.monitoring.coreos.com
kubectl delete crd alertmanagers.monitoring.coreos.com
```

### watch rook-ceph cluster

> [reference](https://gist.github.com/jamesbuckett/659bf0675acd306407a29d90901bce86)

need [import](https://grafana.com/docs/reference/export_import/) corresponding dashboard

- [Ceph-Cluster](https://grafana.com/dashboards/2842)
- [Ceph-OSD](https://grafana.com/dashboards/5336)
- [Ceph-Pools](https://grafana.com/dashboards/5342)

[setup monitor service on rook-ceph](https://github.com/rook/rook/blob/master/Documentation/ceph-monitoring.md)

> https://github.com/coreos/prometheus-operator/blob/master/Documentation/user-guides/getting-started.md

```bash
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/monitoring/service-monitoring.yaml 
servicemonitor.monitoring.coreos.com/rook-ceph-mgr created
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/monitoring/prometheus.yaml 
serviceaccount/prometheus created
clusterrole.rbac.authorization.k8s.io/prometheus created
clusterrole.rbac.authorization.k8s.io/prometheus-rules created
clusterrolebinding.rbac.authorization.k8s.io/prometheus created
prometheus.monitoring.coreos.com/rook-prometheus created
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/monitoring/prometheus-service.yaml 
service/rook-prometheus created

# check svc
➜  cloud git:(master) ✗ kubectl get svc
NAME                              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
prometheus-operated               ClusterIP   None             <none>        9090/TCP            2m54s
rook-ceph-mgr                     ClusterIP   10.98.148.7      <none>        9283/TCP            18h
rook-ceph-mgr-dashboard           ClusterIP   10.107.141.131   <none>        8443/TCP            18h
rook-ceph-mon-a                   ClusterIP   10.103.172.100   <none>        6789/TCP,3300/TCP   18h
rook-ceph-mon-b                   ClusterIP   10.99.57.88      <none>        6789/TCP,3300/TCP   18h
rook-ceph-mon-c                   ClusterIP   10.105.17.141    <none>        6789/TCP,3300/TCP   18h
rook-ceph-rgw-my-store            ClusterIP   10.97.105.1      <none>        80/TCP              17h
rook-ceph-rgw-my-store-external   NodePort    10.106.7.164     <none>        80:31586/TCP        17h
rook-prometheus                   NodePort    10.109.134.158   <none>        9090:30900/TCP      2m46s

# forward prometheus to localhost
➜  cloud git:(master) ✗ kubectl --namespace rook-ceph port-forward svc/rook-prometheus 3000:909
# check on http://localhost:3000
```

but `grafana` is in `monitoring` namespace...

```bash
➜  cloud git:(master) ✗ kubectl get svc --all-namespaces
NAMESPACE       NAME                                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
default         kubernetes                                           ClusterIP   10.96.0.1        <none>        443/TCP             19h
ingress-nginx   default-http-backend                                 ClusterIP   10.98.25.253     <none>        80/TCP              19h
kube-system     kube-dns                                             ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP       19h
kube-system     kubelet                                              ClusterIP   None             <none>        10250/TCP           35m
kube-system     metrics-server                                       ClusterIP   10.98.184.173    <none>        443/TCP             19h
kube-system     test-release-prometheus-op-coredns                   ClusterIP   None             <none>        9153/TCP            20m
kube-system     test-release-prometheus-op-kube-controller-manager   ClusterIP   None             <none>        10252/TCP           20m
kube-system     test-release-prometheus-op-kube-etcd                 ClusterIP   None             <none>        2379/TCP            20m
kube-system     test-release-prometheus-op-kube-scheduler            ClusterIP   None             <none>        10251/TCP           20m
kube-system     test-release-prometheus-op-kubelet                   ClusterIP   None             <none>        10250/TCP           162m
kube-system     tiller-deploy                                        ClusterIP   10.103.248.23    <none>        44134/TCP           19h
monitoring      alertmanager-operated                                ClusterIP   None             <none>        9093/TCP,6783/TCP   25m
monitoring      prometheus-operated                                  ClusterIP   None             <none>        9090/TCP            20m
monitoring      test-release-grafana                                 ClusterIP   10.97.254.118    <none>        80/TCP              20m
monitoring      test-release-kube-state-metrics                      ClusterIP   10.98.118.238    <none>        8080/TCP            20m
monitoring      test-release-prometheus-node-exporter                ClusterIP   10.108.156.169   <none>        9100/TCP            20m
monitoring      test-release-prometheus-op-alertmanager              ClusterIP   10.96.60.122     <none>        9093/TCP            20m
monitoring      test-release-prometheus-op-operator                  ClusterIP   10.108.90.42     <none>        8080/TCP            20m
monitoring      test-release-prometheus-op-prometheus                ClusterIP   10.102.160.22    <none>        9090/TCP            20m
rook-ceph       prometheus-operated                                  ClusterIP   None             <none>        9090/TCP            13m
rook-ceph       rook-ceph-mgr                                        ClusterIP   10.98.148.7      <none>        9283/TCP            18h
rook-ceph       rook-ceph-mgr-dashboard                              ClusterIP   10.107.141.131   <none>        8443/TCP            18h
rook-ceph       rook-ceph-mon-a                                      ClusterIP   10.103.172.100   <none>        6789/TCP,3300/TCP   18h
rook-ceph       rook-ceph-mon-b                                      ClusterIP   10.99.57.88      <none>        6789/TCP,3300/TCP   18h
rook-ceph       rook-ceph-mon-c                                      ClusterIP   10.105.17.141    <none>        6789/TCP,3300/TCP   18h
rook-ceph       rook-ceph-rgw-my-store                               ClusterIP   10.97.105.1      <none>        80/TCP              18h
rook-ceph       rook-ceph-rgw-my-store-external                      NodePort    10.106.7.164     <none>        80:31586/TCP        18h
rook-ceph       rook-prometheus                                      NodePort    10.101.27.248    <none>        9090:30900/TCP      13m
```

and it can NOT access to rook-ceph cluster...

```bash
➜  cloud git:(master) ✗ kubectl --namespace monitoring port-forward svc/test-release-grafana 3000:80
```

i think it's caused by the rbac role binding...

## install prometheus / grafana individually

set prometheus persistent storage class in `prometheus-values.yaml`

```bash
➜  cloud git:(master) ✗ helm install stable/prometheus --name prometheus --namespace monitoring -f prometheus-values.yaml
```

inspect prometheus: `helm inspect stable/prometheus`

disable grafana persistent storage and install it with `grafana-values.yaml`

```bash
➜  cloud git:(master) ✗ helm install --name grafana stable/grafana -f grafana-values.yaml --namespace monitoring
```

grafana secret:

```bash
➜  cloud git:(master) ✗ kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
BPsV8Wn5TlTcztpgFtlxe3dDj9DDC09m3rgrZQLl
```

port forward:

```bash
kubectl port-forward --namespace=monitoring $(kubectl get pods --namespace=monitoring --selector=app=grafana --output=jsonpath='{.items[*].metadata.name}') 3000:3000
```

still can not access to the rook-ceph namespace...

## change rbac role

[Cross Namespace Monitoring using namespaceSelector with kube-prometheus manifests](https://github.com/coreos/prometheus-operator/issues/1921)

failed...

## finally

start prometheus on `rook-ceph` namespace with `.yaml` files in `Rook/monitoring`

start `grafana` on `rook-ceph` namespace with helm: `helm install --name rook-grafana stable/grafana --namespace rook-ceph`

check svc:

```bash
➜  cloud git:(master) ✗ kubectl get svc                 NAME                              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
prometheus-operated               ClusterIP   None             <none>        9090/TCP            6m6s
rook-ceph-mgr                     ClusterIP   10.98.148.7      <none>        9283/TCP            21h
rook-ceph-mgr-dashboard           ClusterIP   10.107.141.131   <none>        8443/TCP            21h
rook-ceph-mon-a                   ClusterIP   10.103.172.100   <none>        6789/TCP,3300/TCP   21h
rook-ceph-mon-b                   ClusterIP   10.99.57.88      <none>        6789/TCP,3300/TCP   21h
rook-ceph-mon-c                   ClusterIP   10.105.17.141    <none>        6789/TCP,3300/TCP   21h
rook-ceph-rgw-my-store            ClusterIP   10.97.105.1      <none>        80/TCP              21h
rook-ceph-rgw-my-store-external   NodePort    10.106.7.164     <none>        80:31586/TCP        20h
rook-grafana                      ClusterIP   10.100.191.58    <none>        80/TCP              19m
rook-prometheus                   NodePort    10.96.166.215    <none>        9000:30900/TCP      5m57s
```

get grafana secret:

```bash
➜  cloud git:(master) ✗ kubectl get secret --namespace rook-ceph rook-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

2QSsnL9Sd7IifQoLLPvplXZwR04XgnGuKogJqI7w

forward port

```bash
➜  cloud git:(master) ✗ kubectl port-forward --namespace=rook-ceph $(kubectl get pods --namespace=rook-ceph --selector=app=grafana --output=jsonpath='{.items[*].metadata.name}') 5000:3000
```

access from `http://localhost:5000`

add `prometheus` data source: `URL: http://10.96.166.215:9000/`

finally it works!

## rook with prometheus-operator

```bash
➜  cloud git:(master) ✗ helm install --name monitor stable/prometheus-operator --namespace rook-ceph
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/monitoring/service-monitoring.yaml
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/monitoring/prometheus.yaml
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/monitoring/prometheus-service.yaml
➜  cloud git:(master) ✗ kubectl apply -f ./Rook/monitoring/prometheus-ceph-rules.yaml
➜  cloud git:(master) ✗ kubectl get svc
NAME                                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
alertmanager-operated                     ClusterIP   None             <none>        9093/TCP,6783/TCP   2m7s
monitor-grafana                           ClusterIP   10.111.168.18    <none>        80/TCP              2m14s
monitor-kube-state-metrics                ClusterIP   10.104.89.49     <none>        8080/TCP            2m14s
monitor-prometheus-node-exporter          ClusterIP   10.106.180.121   <none>        9100/TCP            2m14s
monitor-prometheus-operato-alertmanager   ClusterIP   10.106.211.18    <none>        9093/TCP            2m14s
monitor-prometheus-operato-operator       ClusterIP   10.111.42.200    <none>        8080/TCP            2m14s
monitor-prometheus-operato-prometheus     ClusterIP   10.107.254.45    <none>        9090/TCP            2m14s
prometheus-operated                       ClusterIP   None             <none>        9090/TCP            2m1s
rook-ceph-mgr                             ClusterIP   10.98.148.7      <none>        9283/TCP            22h
rook-ceph-mgr-dashboard                   ClusterIP   10.107.141.131   <none>        8443/TCP            22h
rook-ceph-mon-a                           ClusterIP   10.103.172.100   <none>        6789/TCP,3300/TCP   23h
rook-ceph-mon-b                           ClusterIP   10.99.57.88      <none>        6789/TCP,3300/TCP   23h
rook-ceph-mon-c                           ClusterIP   10.105.17.141    <none>        6789/TCP,3300/TCP   22h
rook-ceph-rgw-my-store                    ClusterIP   10.97.105.1      <none>        80/TCP              22h
rook-ceph-rgw-my-store-external           NodePort    10.106.7.164     <none>        80:31586/TCP        22h
rook-prometheus                           NodePort    10.100.151.118   <none>        9000:30900/TCP      54s
➜  cloud git:(master) ✗ kubectl get secret --namespace rook-ceph mornitor-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
prom-operator
➜  cloud git:(master) ✗ kubectl --namespace rook-ceph port-forward svc/monitor-grafana 3000:80
```

add rook prometheus data source to grafana (`http://10.100.151.118:9000`)

add `Ceph-Cluster` (2842), `Ceph-OSD` (5336), `Ceph-Pool` (5342)

now, one grafana can monitor all
