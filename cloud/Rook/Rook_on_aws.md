#

## create new cluster

find details in `aws.md` and `pharos.md`

**warn**: take care of the instance route tables config

after successfully creating the k8s cluster, the following message will show up:

```bash
==> Cluster has been crafted! (took 3 minutes 9 seconds)
    To configure kubectl for connecting to the cluster, use:
      pharos kubeconfig -c cluster.yml  -n aged-water-6535 > kubeconfig
      export KUBECONFIG=./kubeconfig

➜  Rook git:(master) ✗ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   25m
➜  Rook git:(master) ✗ kubectl get nodes
NAME            STATUS   ROLES    AGE   VERSION
ip-10-0-0-180   Ready    worker   25m   v1.13.6
ip-10-0-0-222   Ready    master   25m   v1.13.6
ip-10-0-0-64    Ready    worker   25m   v1.13.6

➜  Rook git:(master) ✗ kubectl cluster-info     
Kubernetes master is running at https://xxx:6443
KubeDNS is running at https://xxx:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://xxx:6443/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy
```

## deploy rook operator on cluster

- disk storage should be larger than 40GB
- `kubectl create -f ./example_yaml/common.yaml`
- `kubectl create -f ./example_yaml/operator.yaml`
- check namespaces `kubectl get namespaces`

```bash
➜  Rook git:(master) ✗ kubectl get namespaces
NAME            STATUS   AGE
default         Active   44m
ingress-nginx   Active   26m
kube-public     Active   44m
kube-system     Active   44m
rook-ceph       Active   9m10s
```

- **strange problem**: `kube-controller-manager` and `kube-scheduler` on master node keep `CrashLoopBackOff`
  - check on master node: `sudo docker ps -a | grep kube-controller-manager`, `ps -aux | grep controller`, `netstat`
  - maybe this is due to my instance config is too poor? (t2 micro...)
  - after restart for 12-13 times, both controller and scheduler are in running status...
  - then finally other deployments can run
- **warn**: after changing instance from micro to small (worker node) and medium (master node), this succeeds very smoothly... (**WTF**) controller and scheduler will not restart again and again...

- verify rook-ceph-operator, rook-ceph-agent and rook-discover pods are in `Running` status
  - `kubectl -n rook-ceph get pod`
  - `kubectl get pods --all-namespaces`

- rook-ceph-operator at `ContainerCreating` status...
  - > https://github.com/rook/rook/blob/master/Documentation/common-issues.md
  - `kubectl describe -f ./example_yaml/operator.yaml`
  - `kubectl describe pod -l name=rook-ceph-operator-8bc78b546-zb4zw`
  - `kubectl logs -n rook-ceph -l app=rook-ceph-operator`
  - still do NOT know why... but i think it has some relationship with Pharos because they has a kontena storage (depends on Rook/Ceph) for Pro/EE users...

## Use KOPS instead of Pharos

- create cluster as stated in `kops.md`
- `kubectl create --save-config -f common.yaml`, `kubectl create --save-config -f operator.yaml`

    ```bash
    ➜  cloud git:(master) ✗ kubectl get pods --all-namespaces
    NAMESPACE     NAME                                                    READY   STATUS    RESTARTS   AGE
    kube-system   dns-controller-6d6b7f78b-q7rjs                          1/1     Running   0          10m
    kube-system   etcd-server-events-ip-172-20-50-218.ec2.internal        1/1     Running   0          9m
    kube-system   etcd-server-ip-172-20-50-218.ec2.internal               1/1     Running   0          9m
    kube-system   kube-apiserver-ip-172-20-50-218.ec2.internal            1/1     Running   1          10m
    kube-system   kube-controller-manager-ip-172-20-50-218.ec2.internal   1/1     Running   0          9m
    kube-system   kube-dns-5fbcb4d67b-rqtj7                               3/3     Running   0          8m
    kube-system   kube-dns-5fbcb4d67b-tjqch                               3/3     Running   0          10m
    kube-system   kube-dns-autoscaler-6874c546dd-mdd6r                    1/1     Running   0          10m
    kube-system   kube-proxy-ip-172-20-38-34.ec2.internal                 1/1     Running   0          8m
    kube-system   kube-proxy-ip-172-20-39-124.ec2.internal                1/1     Running   0          8m
    kube-system   kube-proxy-ip-172-20-50-218.ec2.internal                1/1     Running   0          10m
    kube-system   kube-proxy-ip-172-20-55-92.ec2.internal                 1/1     Running   0          9m
    kube-system   kube-scheduler-ip-172-20-50-218.ec2.internal            1/1     Running   0          10m
    rook-ceph     rook-ceph-agent-mr94g                                   1/1     Running   0          5m
    rook-ceph     rook-ceph-agent-t22qx                                   1/1     Running   0          5m
    rook-ceph     rook-ceph-agent-zb5lr                                   1/1     Running   0          5m
    rook-ceph     rook-ceph-operator-f655d9644-pwmbv                      1/1     Running   0          5m
    rook-ceph     rook-discover-7rqh2                                     1/1     Running   0          5m
    rook-ceph     rook-discover-dfmcd                                     1/1     Running   0          5m
    rook-ceph     rook-discover-mmswt                                     1/1     Running   0          5m
    ```
- successfully create `rook-ceph` on cluster...
- `kubectl create --save-config -f cluster.yaml`
  - try to change the CPU and RAM config in `cluster.yaml`, but got this error log: `2019-05-16 06:11:16.848773 E | op-cluster: failed to create cluster in namespace rook-ceph. failed to start the mons. refuse to run the pod with 512mb of ram, provide at least 1024mb.` Re-config it and `kubectl apply -f cluster.yaml`
  - watch the log: `watch "kubectl logs -n rook-ceph -l app=rook-ceph-operator"`

    ```bash
    ➜  cloud git:(master) ✗ kubectl get pods --namespace rook-ceph
    NAME                                                        READY   STATUS      RESTARTS   AGE
    rook-ceph-agent-mr94g                                       1/1     Running     0          9m
    rook-ceph-agent-t22qx                                       1/1     Running     0          9m
    rook-ceph-agent-zb5lr                                       1/1     Running     0          9m
    rook-ceph-mgr-a-79bc7f644d-vhl4v                            1/1     Running     0          1m
    rook-ceph-mon-a-75c98f4456-9mnmj                            1/1     Running     0          1m
    rook-ceph-mon-b-5d5c5575ff-xbvbf                            1/1     Running     0          1m
    rook-ceph-mon-c-6b4b77776c-2gs6c                            1/1     Running     0          1m
    rook-ceph-operator-f655d9644-pwmbv                          1/1     Running     0          10m
    rook-ceph-osd-prepare-ip-172-20-38-34.ec2.internal-646jg    0/2     Completed   1          49s
    rook-ceph-osd-prepare-ip-172-20-39-124.ec2.internal-h6llt   0/2     Completed   1          49s
    rook-ceph-osd-prepare-ip-172-20-55-92.ec2.internal-j77k6    0/2     Completed   1          49s
    rook-discover-7rqh2                                         1/1     Running     0          9m
    rook-discover-dfmcd                                         1/1     Running     0          9m
    rook-discover-mmswt                                         1/1     Running     0          9m
    ```
- next define Rook storage Pool and StorageClass, use 3 replicas since has 3 OSDs
  - `kubectl create -f storageclass.yaml`
- install Rook tool box to have better visibility
  - `kubectl create -f toolbox.yaml`
    - `deployment.apps/rook-ceph-tools created`
    - create this pod `rook-ceph-tools-848bc49f54-jnrr2                            1/1     Running     0          21s`
  - `kubectl -n rook-ceph exec -it rook-ceph-tools-848bc49f54-jnrr2 -- bash`
    - > https://rook.io/docs/rook/v1.0/ceph-toolbox.html
    - `ceph status`

    ```bash
    [root@ip-172-20-55-92 /]# ceph status
    cluster:
        id:     64aa880e-c4c2-4268-9c9d-1aa9d9b49add
        health: HEALTH_WARN
                Reduced data availability: 100 pgs inactive

    services:
        mon: 3 daemons, quorum a,b,c (age 21m)
        mgr: a(active, since 21m)
        osd: 0 osds: 0 up, 0 in

    data:
        pools:   1 pools, 100 pgs
        objects: 0 objects, 0 B
        usage:   0 B used, 0 B / 0 B avail
        pgs:     100.000% pgs unknown
                100 unknown
    ```

    - `ceph df`

    ```bash
    [root@ip-172-20-55-92 /]# ceph df
    RAW STORAGE:
        CLASS     SIZE     AVAIL     USED     RAW USED     %RAW USED
        TOTAL      0 B       0 B      0 B          0 B             0

    POOLS:
        POOL            ID     STORED     OBJECTS     USED     %USED     MAX AVAIL
        replicapool      1        0 B           0      0 B         0           0 B
    ```

    - `rados df`

    ```bash
    [root@ip-172-20-55-92 /]# rados df
    POOL_NAME   USED OBJECTS CLONES COPIES MISSING_ON_PRIMARY UNFOUND DEGRADED RD_OPS  RD WR_OPS  WR USED COMPR UNDER COMPR 
    replicapool  0 B       0      0      0                  0       0        0      0 0 B      0 0 B        0 B         0 B

    total_objects    0
    total_used       0 B
    total_avail      0 B
    total_space      0 B
    ```

    - data 100 unknown with this `HEALTH WARN`
      - > http://docs.ceph.com/docs/master/rados/troubleshooting/troubleshooting-pg/
      - `ceph health detail`

        ```bash
        [root@ip-172-20-55-92 /]# ceph health detail
        HEALTH_WARN Reduced data availability: 100 pgs inactive
        PG_AVAILABILITY Reduced data availability: 100 pgs inactive
            pg 1.0 is stuck inactive for 1365.495980, current state unknown, last acting []
            ...
        ```

      - [peering problem for `stuck inactive` pg](http://docs.ceph.com/docs/master/rados/troubleshooting/troubleshooting-pg/#stuck-placement-groups)
      - from former pod info, osd-prepare NOT ready and hang there... need find the reason
  - upgrade kops to latest version (1.12.0) to enable using t3 instances on aws
    - rook-ceph stuck at `rook-ceph-detect-version`, have to delete it -> `kubectl -n rook-ceph delete job rook-ceph-detect-version`
    - now stuck at `op-cluster: unknown ceph major version. failed to complete version job. failed to detect job . jobs.batch "rook-ceph-detect-version" not found`
    - delete all rook-ceph pods
    - re-create all pods
    - still stuck at this job...