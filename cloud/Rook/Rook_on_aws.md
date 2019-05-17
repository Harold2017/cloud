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
    - > https://github.com/rook/rook/issues/3081
    - change to default cluster yaml, this annoying `version-detect` disappeared but now stuck at `osd-prepare`

    ```bash
    rook-ceph     rook-ceph-osd-prepare-ip-172-20-33-166.ec2.internal-j7dx8   0/2     Completed   0          11m
    rook-ceph     rook-ceph-osd-prepare-ip-172-20-44-132.ec2.internal-d65gf   0/2     Completed   0          11m
    rook-ceph     rook-ceph-osd-prepare-ip-172-20-61-242.ec2.internal-2ldkg   0/2     Completed   0          11m
    ```

    - investigate pod logs
      - seems `copy-bins` works well

        ```bash
        ➜  Rook git:(master) ✗ kubectl logs -n rook-ceph -f rook-ceph-osd-prepare-ip-172-20-33-166.ec2.internal-j7dx8 copy-bins
        2019-05-17 02:23:20.505106 I | cephosd: copying /usr/local/bin/rook to /rook/rook
        2019-05-17 02:23:20.574001 I | cephosd: copying /tini to /rook/tini
        2019-05-17 02:23:20.574431 I | cephcmd: successfully copied rook binaries
        ```

      - but `provision` **NOT**

        ```bash
        ➜  Rook git:(master) ✗ kubectl logs -n rook-ceph -f rook-ceph-osd-prepare-ip-172-20-33-166.ec2.internal-j7dx8 provision 
        2019-05-17 02:23:20.735536 I | rookcmd: starting Rook v1.0.0-38.g0c23e1c with arguments '/rook/rook ceph osd provision'
        2019-05-17 02:23:20.735616 I | rookcmd: flag values: --cluster-id=9050935a-784a-11e9-924d-0a36eb67a442, --data-device-filter=all, --data-devices=, --data-directories=, --encrypted-device=false, --force-format=false, --help=false, --location=, --log-flush-frequency=5s, --log-level=INFO, --metadata-device=, --node-name=ip-172-20-33-166.ec2.internal, --osd-database-size=20480, --osd-journal-size=5120, --osd-store=, --osd-wal-size=576, --osds-per-device=1
        2019-05-17 02:23:20.735623 I | op-mon: parsing mon endpoints: c=100.66.233.2:6789,a=100.69.53.6:6789,b=100.66.166.94:6789
        2019-05-17 02:23:20.752375 W | cephconfig: failed to add config file override from '/etc/rook/config/override.conf': open /etc/rook/config/override.conf: no such file or directory
        2019-05-17 02:23:20.752395 I | cephconfig: writing config file /var/lib/rook/rook-ceph/rook-ceph.config
        2019-05-17 02:23:20.752698 I | cephconfig: copying config to /etc/ceph/ceph.conf
        2019-05-17 02:23:20.752803 I | cephconfig: generated admin config in /var/lib/rook/rook-ceph
        2019-05-17 02:23:20.752892 I | cephosd: discovering hardware
        2019-05-17 02:23:20.752900 I | exec: Running command: lsblk --all --noheadings --list --output KNAME
        2019-05-17 02:23:20.761413 I | exec: Running command: lsblk /dev/nvme0n1 --bytes --nodeps --pairs --output SIZE,ROTA,RO,TYPE,PKNAME
        2019-05-17 02:23:20.763570 I | exec: Running command: sgdisk --print /dev/nvme0n1
        2019-05-17 02:23:20.767367 I | exec: Running command: udevadm info --query=property /dev/nvme0n1
        2019-05-17 02:23:20.789254 I | exec: Running command: lsblk /dev/nvme0n1p1 --bytes --nodeps --pairs --output SIZE,ROTA,RO,TYPE,PKNAME
        2019-05-17 02:23:20.791964 I | exec: Running command: udevadm info --query=property /dev/nvme0n1p1
        2019-05-17 02:23:20.794442 I | exec: Running command: lsblk /dev/nvme0n1p2 --bytes --nodeps --pairs --output SIZE,ROTA,RO,TYPE,PKNAME
        2019-05-17 02:23:20.796406 I | exec: Running command: udevadm info --query=property /dev/nvme0n1p2
        2019-05-17 02:23:20.798274 I | cephosd: creating and starting the osds
        2019-05-17 02:23:20.798292 I | exec: Running command: lsblk /dev/nvme0n1 --bytes --pairs --output NAME,SIZE,TYPE,PKNAME
        2019-05-17 02:23:20.799905 I | exec: Running command: udevadm info --query=property /dev/nvme0n1p1
        2019-05-17 02:23:20.801293 I | exec: Running command: udevadm info --query=property /dev/nvme0n1p2
        2019-05-17 02:23:20.802917 I | sys: non-rook partition: primary
        2019-05-17 02:23:20.802931 I | sys: non-rook partition: root
        2019-05-17 02:23:20.802939 I | exec: Running command: udevadm info --query=property /dev/nvme0n1
        2019-05-17 02:23:20.804460 I | cephosd: skipping device nvme0n1 that is in use (not by rook). fs: , ownPartitions: false
        2019-05-17 02:23:20.808885 I | cephosd: configuring osd devices: {"Entries":{}}
        2019-05-17 02:23:20.808900 I | exec: Running command: ceph-volume lvm batch --prepare
        2019-05-17 02:23:21.109021 I | cephosd: no more devices to configure
        2019-05-17 02:23:21.109048 I | exec: Running command: ceph-volume lvm list --format json
        2019-05-17 02:23:22.043304 I | cephosd: 0 ceph-volume osd devices configured on this node
        2019-05-17 02:23:22.043330 I | cephosd: devices = []
        2019-05-17 02:23:22.046627 I | cephosd: configuring osd dirs: map[]
        2019-05-17 02:23:22.046816 I | cephosd: removing osd devices: {"metadata":null,"entries":[]}
        2019-05-17 02:23:22.046847 I | cephosd: removing osd dirs: map[]
        2019-05-17 02:23:22.046852 I | cephosd: saving osd dir map
        2019-05-17 02:23:22.046857 I | cephosd: device osds:[]
        dir osds: []
        ```

      - seems **NO** device for it to config ceph but it should use dir instead, why stuck? after investigating rool-discover pod, the disk is **discovered**

        ```bash
        ➜  Rook git:(master) ✗ kubectl logs -n rook-ceph -f rook-discover-5snwr
        2019-05-17 02:21:22.736374 I | rookcmd: starting Rook v1.0.0-38.g0c23e1c with arguments '/usr/local/bin/rook discover --discover-interval 60m'
        2019-05-17 02:21:22.736431 I | rookcmd: flag values: --discover-interval=1h0m0s, --help=false, --log-flush-frequency=5s, --log-level=INFO
        2019-05-17 02:21:22.737325 I | rook-discover: device discovery interval is 1h0m0s
        2019-05-17 02:21:22.737393 I | rook-discover: updating device configmap
        2019-05-17 02:21:22.737427 I | exec: Running command: lsblk --all --noheadings --list --output KNAME
        2019-05-17 02:21:22.742170 I | exec: Running command: lsblk /dev/nvme0n1 --bytes --nodeps --pairs --output SIZE,ROTA,RO,TYPE,PKNAME
        2019-05-17 02:21:22.743736 I | exec: Running command: sgdisk --print /dev/nvme0n1
        2019-05-17 02:21:22.745642 I | exec: Running command: udevadm info --query=property /dev/nvme0n1
        2019-05-17 02:21:22.749310 I | exec: Running command: lsblk /dev/nvme0n1p1 --bytes --nodeps --pairs --output SIZE,ROTA,RO,TYPE,PKNAME
        2019-05-17 02:21:22.752586 I | exec: Running command: udevadm info --query=property /dev/nvme0n1p1
        2019-05-17 02:21:22.753719 I | exec: Running command: lsblk /dev/nvme0n1p2 --bytes --nodeps --pairs --output SIZE,ROTA,RO,TYPE,PKNAME
        2019-05-17 02:21:22.755051 I | exec: Running command: udevadm info --query=property /dev/nvme0n1p2
        2019-05-17 02:21:22.756424 I | exec: Running command: lsblk /dev/nvme0n1 --bytes --pairs --output NAME,SIZE,TYPE,PKNAME
        2019-05-17 02:21:22.757946 I | exec: Running command: udevadm info --query=property /dev/nvme0n1p1
        2019-05-17 02:21:22.759117 I | exec: Running command: udevadm info --query=property /dev/nvme0n1p2
        2019-05-17 02:21:22.760184 I | exec: Running command: udevadm info --query=property /dev/nvme0n1
        2019-05-17 02:21:22.761286 I | rook-discover: available devices: [{Name:nvme0n1 Parent: HasChildren:false DevLinks:/dev/disk/by-id/nvme-Amazon_Elastic_Block_Store_vol0a13de76620f5f4df /dev/disk/by-id/nvme-nvme.1d0f-766f6c3061313364653736363230663566346466-416d617a6f6e20456c617374696320426c6f636b2053746f7265-00000001 /dev/disk/by-path/pci-0000:00:04.0-nvme-1 Size:137438953472 UUID:5a25fbfe-16d2-4ca8-a641-155dba52c20a Serial:Amazon Elastic Block Store_vol0a13de76620f5f4df Type:disk Rotational:false Readonly:false Partitions:[{Name:nvme0n1p1 Size:1031680 Label:primary Filesystem:} {Name:nvme0n1p2 Size:137437887488 Label:root Filesystem:ext4}] Filesystem: Vendor: Model: WWN: WWNVendorExtension: Empty:false}]
        ```

      - loop up the configmaps, what is this `root-test-ownerref`?

        ```bash
        ➜  Rook git:(master) ✗ kubectl -n rook-ceph get cm
        NAME                                         DATA   AGE
        local-device-ip-172-20-33-166.ec2.internal   1      44m
        local-device-ip-172-20-44-132.ec2.internal   1      44m
        local-device-ip-172-20-61-242.ec2.internal   1      44m
        rook-ceph-config                             1      43m
        rook-ceph-mon-endpoints                      3      43m
        rook-config-override                         1      43m
        rook-crush-config                            1      42m
        rook-test-ownerref                           0      43m
        ```

      - change `cluster_default.yaml` to set the storage dir config

        ```bash
        storage:
            useAllNodes: true
            useAllDevices: true
            deviceFilter:
            location:
            config:
            storeType: filestore
            databaseSizeMB: "1024" # uncomment if the disks are smaller than 100 GB
            journalSizeMB: "1024"  # uncomment if the disks are 20 GB or smaller
            osdsPerDevice: "1"
            directories:
            - path: /var/lib/rook
        ```

        - `rook-ceph-operator` stuck at `op-mon`

        ```bash
        2019-05-17 04:06:42.842327 I | op-mon: mons running: [a]
        2019-05-17 04:06:42.842442 I | exec: Running command: ceph mon_status --connect-timeout=15 --cluster=rook-ceph --conf=/var/lib/rook/rook-ce
        ph/rook-ceph.config --keyring=/var/lib/rook/rook-ceph/client.admin.keyring --format json --out-file /tmp/669419223
        2019-05-17 04:06:57.925583 I | exec: timed out
        ```

      - this issue has the same problem with mine: https://github.com/rook/rook/issues/3135
        - **strange**: after comment `journalSizeMB: "1024"`, it works... so it really matters due to my disk size is 100GB...
  
        ```bash
        rook-ceph     rook-ceph-agent-l5dxn                                       1/1     Running     0          4m7s
        rook-ceph     rook-ceph-agent-rtljm                                       1/1     Running     0          4m7s
        rook-ceph     rook-ceph-agent-wdz78                                       1/1     Running     0          4m7s
        rook-ceph     rook-ceph-mgr-a-7954598d69-hv74h                            1/1     Running     0          86s
        rook-ceph     rook-ceph-mon-a-79dc4fd9d4-llkcb                            1/1     Running     0          2m3s
        rook-ceph     rook-ceph-mon-b-84896f6b5d-ch2wr                            1/1     Running     0          115s
        rook-ceph     rook-ceph-mon-c-dbb9d7f5d-c8gjn                             1/1     Running     0          103s
        rook-ceph     rook-ceph-operator-7b976856bf-zhpnx                         1/1     Running     0          4m34s
        rook-ceph     rook-ceph-osd-0-7557dd7cf5-xx7jd                            1/1     Running     0          56s
        rook-ceph     rook-ceph-osd-1-58456c9875-vz4f6                            1/1     Running     0          56s
        rook-ceph     rook-ceph-osd-2-6b66bdcd89-pqcfs                            1/1     Running     0          55s
        rook-ceph     rook-ceph-osd-prepare-ip-172-20-35-247.ec2.internal-hhmps   0/2     Completed   0          62s
        rook-ceph     rook-ceph-osd-prepare-ip-172-20-55-182.ec2.internal-sxtvj   0/2     Completed   1          62s
        rook-ceph     rook-ceph-osd-prepare-ip-172-20-63-39.ec2.internal-44wxl    0/2     Completed   0          62s
        rook-ceph     rook-discover-njszt                                         1/1     Running     0          4m7s
        rook-ceph     rook-discover-qm2mg                                         1/1     Running     0          4m7s
        rook-ceph     rook-discover-tgkd7                                         1/1     Running     0          4m7s
        ```

      - **finally works!**

        ```bash
        ➜  Rook git:(master) ✗ kubectl -n rook-ceph exec -it rook-ceph-tools-689646bb64-jbfzz bash
        bash: warning: setlocale: LC_CTYPE: cannot change locale (en_US.UTF-8): No such file or directory
        bash: warning: setlocale: LC_COLLATE: cannot change locale (en_US.UTF-8): No such file or directory
        bash: warning: setlocale: LC_MESSAGES: cannot change locale (en_US.UTF-8): No such file or directory
        bash: warning: setlocale: LC_NUMERIC: cannot change locale (en_US.UTF-8): No such file or directory
        bash: warning: setlocale: LC_TIME: cannot change locale (en_US.UTF-8): No such file or directory
        [root@ip-172-20-35-247 /]# ceph status
        cluster:
            id:     0a543ab8-c956-4269-bc92-645741d079f0
            health: HEALTH_OK

        services:
            mon: 3 daemons, quorum a,b,c (age 33m)
            mgr: a(active, since 32m)
            osd: 3 osds: 3 up (since 32m), 3 in (since 32m)

        data:
            pools:   0 pools, 0 pgs
            objects: 0 objects, 0 B
            usage:   42 GiB used, 318 GiB / 360 GiB avail
            pgs:
        ```

      - my cluster config: t3.medium as master, 3 t3.small as node, master volume size 64GB, node voulmn size 128GB
