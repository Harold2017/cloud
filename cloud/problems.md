#

## lots of pods down after weekend... (node lost)

```bash
NAME                            STATUS     ROLES    AGE     VERSION
ip-172-20-35-247.ec2.internal   NotReady   node     10d     v1.12.7
ip-172-20-38-207.ec2.internal   NotReady   node     4d18h   v1.12.7
ip-172-20-57-215.ec2.internal   Ready      master   10d     v1.12.7
ip-172-20-63-39.ec2.internal    Ready      node     10d     v1.12.7

# ip-172-20-35-247.ec2.internal
Conditions:
  Type                 Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----                 ------  -----------------                 ------------------                ------                       -------
  OutOfDisk            False   Mon, 27 May 2019 12:18:33 +0800   Thu, 23 May 2019 18:19:38 +0800   KubeletHasSufficientDisk     kubelet has sufficient disk space available
  MemoryPressure       False   Mon, 27 May 2019 12:18:33 +0800   Thu, 23 May 2019 18:19:38 +0800   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         False   Mon, 27 May 2019 12:18:33 +0800   Thu, 23 May 2019 18:19:38 +0800   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure          False   Mon, 27 May 2019 12:18:33 +0800   Fri, 17 May 2019 12:21:55 +0800   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready                False   Mon, 27 May 2019 12:18:33 +0800   Thu, 23 May 2019 18:19:38 +0800   KubeletNotReady              container runtime is down,PLEG is not healthy: pleg was last seen active 90h19m2.187972815s ago; threshold is 3m0s

Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource                    Requests      Limits
  --------                    --------      ------
  cpu                         910m (45%)    668m (33%)
  memory                      1356Mi (72%)  820Mi (43%)
  ephemeral-storage           0 (0%)        0 (0%)
  attachable-volumes-aws-ebs  0             0
Events:
  Type     Reason             Age                      From                                    Message
  ----     ------             ----                     ----                                    -------
  Warning  ContainerGCFailed  4m1s (x5398 over 3d20h)  kubelet, ip-172-20-35-247.ec2.internal  rpc error: code = Unknown desc = Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?


# ip-172-20-38-207.ec2.internal
Conditions:
  Type                 Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----                 ------  -----------------                 ------------------                ------                       -------
  OutOfDisk            False   Mon, 27 May 2019 12:28:23 +0800   Fri, 24 May 2019 13:47:27 +0800   KubeletHasSufficientDisk     kubelet has sufficient disk space available
  MemoryPressure       False   Mon, 27 May 2019 12:28:23 +0800   Fri, 24 May 2019 13:47:27 +0800   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         False   Mon, 27 May 2019 12:28:23 +0800   Fri, 24 May 2019 13:47:27 +0800   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure          False   Mon, 27 May 2019 12:28:23 +0800   Wed, 22 May 2019 18:11:55 +0800   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready                False   Mon, 27 May 2019 12:28:23 +0800   Fri, 24 May 2019 13:47:27 +0800   KubeletNotReady              container runtime is down,PLEG is not healthy: pleg was last seen active 71h14m9.09312227s ago; threshold is 3m0s

Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource                    Requests      Limits
  --------                    --------      ------
  cpu                         1290m (64%)   1068m (53%)
  memory                      1326Mi (71%)  1540Mi (82%)
  ephemeral-storage           0 (0%)        0 (0%)
  attachable-volumes-aws-ebs  0             0
Events:
  Type     Reason             Age                       From                                    Message
  ----     ------             ----                      ----                                    -------
  Warning  ContainerGCFailed  3m20s (x4242 over 3d21h)  kubelet, ip-172-20-38-207.ec2.internal  rpc error: code = Unknown desc = Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

docker daemon crashed

```bash
admin@ip-172-20-38-207:~$ sudo dockerd
Error starting daemon: pid file found, ensure docker is not running or delete /var/run/docker.pid

admin@ip-172-20-38-207:~$ cat /var/run/docker.pid
8208

admin@ip-172-20-38-207:~$ ps -aux | grep docker
root      5491  0.0  0.0   7496  1192 ?        Sl   May23   0:25 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/36fa69e7e3f63ba8706728f1d943709a371b03c88a5c4f74eee284fdcc534ea6 -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root      8781  0.0  0.0   7560  1148 ?        Sl   May23   0:15 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/12b8732cb85db7e3dbe83c45157577d683df280b529a9a26e76541646c6203b1 -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root     17527  0.0  0.1   7496  3260 ?        Sl   May23   0:19 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/402e61702d10c2b648637d777329c1e85060ed318503956925114605dc134f5d -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root     18609  0.0  0.1   7560  3000 ?        Sl   May23   0:21 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/a7b17aa3383e97a626a814d09d2125315e1f8c49ab74dc3cdc70ba16779b3577 -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root     18633  0.0  0.1   7496  3116 ?        Sl   May23   0:10 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/3bf5b5152eecbd768a04989e3218313cfea5917bebaebc17a4e3de11294892d8 -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root     18735  0.0  0.1   8904  3148 ?        Sl   May23   0:08 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/d2eb3381d85b4b9d71b508fb73501ec9cf042d1404511390d94c26da884506af -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root     18767  0.0  0.1   7496  2952 ?        Sl   May23   0:15 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/df516d593675137607fbf9e7c92570b578163cbeb3fea8c564cfe57fa970347b -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root     26106  0.0  0.1  19636  3060 ?        Ss   06:09   0:00 /bin/bash /opt/kubernetes/helpers/docker-healthcheck
root     26585  0.0  0.1  39592  2204 ?        S    06:11   0:00 systemctl start docker
root     26587  0.1  3.2 398884 65160 ?        Ssl  06:11   0:03 /usr/bin/dockerd -H fd:// --ip-masq=false --iptables=false --log-driver=json-file --log-level=warn --log-opt=max-file=5 --log-opt=max-size=10m --storage-driver=overlay2
root     26594  0.1  1.7 351764 34396 ?        Ssl  06:11   0:06 docker-containerd --config /var/run/docker/containerd/containerd.toml
root     26612  0.0  1.3 199100 27520 ?        Ssl  06:11   0:00 /usr/bin/docker run -v /:/rootfs/ -v /var/run/dbus:/var/run/dbus -v /run/systemd:/run/systemd --net=host --pid=host --privileged --env KUBECONFIG=/rootfs/var/lib/kops/kubeconfig -e AWS_REGION=us-east-1 protokube:1.12.0 /usr/bin/protokube --channels=s3://harold-kops-state/harold.k8s.local/addons/bootstrap-channel.yaml --cloud=aws --containerized=true --dns-internal-suffix=internal.harold.k8s.local --dns=gossip --etcd-backup-store=s3://harold-kops-state/harold.k8s.local/backups/etcd/main --etcd-image=k8s.gcr.io/etcd:3.2.24 --initialize-rbac=true --manage-etcd=true --master=false --peer-ca=/srv/kubernetes/ca.crt --peer-cert=/srv/kubernetes/etcd-peer.pem --peer-key=/srv/kubernetes/etcd-peer-key.pem --tls-auth=true --tls-ca=/srv/kubernetes/ca.crt --tls-cert=/srv/kubernetes/etcd.pem --tls-key=/srv/kubernetes/etcd-key.pem --v=4
admin    29510  0.0  0.0  12752   944 pts/0    S+   07:05   0:00 grep docker
root     30291  0.0  0.0   7496  1268 ?        Sl   May24   0:06 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/29ecfe7dc59604a86c41d30a5d9f4a29f0fde943bba5cd40bddcdcb995337045 -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root     30452  0.0  0.1   7496  2624 ?        Sl   May24   0:07 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/ede242f2a3cc2662d0944a0b20522cf7cb7107c0cb91dff98a58c8efc038c7de -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
nobody   30787  0.0  0.3  55452  6796 ?        Ssl  May24   0:01 docker-runc init

admin@ip-172-20-38-207:~$ sudo dockerd
INFO[2019-05-27T06:06:15.168299121Z] libcontainerd: docker-containerd is still running  pid=25657
INFO[2019-05-27T06:06:15.168369401Z] parsed scheme: "unix"                         module=grpc
INFO[2019-05-27T06:06:15.168381713Z] scheme "unix" not registered, fallback to default scheme  module=grpc
INFO[2019-05-27T06:06:15.168418097Z] ccResolverWrapper: sending new addresses to cc: [{unix:///var/run/docker/containerd/docker-containerd.sock 0  <nil>}]  module=grpc
INFO[2019-05-27T06:06:15.168430363Z] ClientConn switching balancer to "pick_first"  module=grpc
INFO[2019-05-27T06:06:15.168490893Z] pickfirstBalancer: HandleSubConnStateChange: 0xc42003b8f0, CONNECTING  module=grpc
WARN[2019-05-27T06:06:35.168717702Z] grpc: addrConn.createTransport failed to connect to {unix:///var/run/docker/containerd/docker-containerd.sock 0  <nil>}. Err :connection error: desc = "transport: error while dialing: dial unix:///var/run/docker/containerd/docker-containerd.sock: timeout". Reconnecting...  module=grpc
INFO[2019-05-27T06:06:35.168804521Z] pickfirstBalancer: HandleSubConnStateChange: 0xc42003b8f0, TRANSIENT_FAILURE  module=grpc
INFO[2019-05-27T06:06:35.168922909Z] pickfirstBalancer: HandleSubConnStateChange: 0xc42003b8f0, CONNECTING  module=grpc

# remove containerd
admin@ip-172-20-38-207:/var/run$ sudo ls docker/
containerd  libnetwork  metrics.sock  netns  plugins  runtime-runc  swarm
admin@ip-172-20-38-207:/var/run$ sudo ls docker/containerd
12b8732cb85db7e3dbe83c45157577d683df280b529a9a26e76541646c6203b1
29ecfe7dc59604a86c41d30a5d9f4a29f0fde943bba5cd40bddcdcb995337045
36fa69e7e3f63ba8706728f1d943709a371b03c88a5c4f74eee284fdcc534ea6
3bf5b5152eecbd768a04989e3218313cfea5917bebaebc17a4e3de11294892d8
402e61702d10c2b648637d777329c1e85060ed318503956925114605dc134f5d
a7b17aa3383e97a626a814d09d2125315e1f8c49ab74dc3cdc70ba16779b3577
containerd.toml
d2eb3381d85b4b9d71b508fb73501ec9cf042d1404511390d94c26da884506af
daemon
df516d593675137607fbf9e7c92570b578163cbeb3fea8c564cfe57fa970347b
docker-containerd-debug.sock
docker-containerd.pid
docker-containerd.sock
ede242f2a3cc2662d0944a0b20522cf7cb7107c0cb91dff98a58c8efc038c7de
admin@ip-172-20-38-207:/var/run$ sudo rm -rf docker/containerd
admin@ip-172-20-38-207:/var/run$ sudo mkdir docker/containerd
admin@ip-172-20-38-207:/var/run$ sudo dockerd
INFO[2019-05-27T07:12:10.179984472Z] libcontainerd: started new docker-containerd process  pid=29903
INFO[2019-05-27T07:12:10.180219627Z] parsed scheme: "unix"                         module=grpc
INFO[2019-05-27T07:12:10.180278403Z] scheme "unix" not registered, fallback to default scheme  module=grpc
INFO[2019-05-27T07:12:10.180324381Z] ccResolverWrapper: sending new addresses to cc: [{unix:///var/run/docker/containerd/docker-containerd.sock 0  <nil>}]  module=grpc
INFO[2019-05-27T07:12:10.180396168Z] ClientConn switching balancer to "pick_first"  module=grpc
INFO[2019-05-27T07:12:10.180468299Z] pickfirstBalancer: HandleSubConnStateChange: 0xc4203605a0, CONNECTING  module=grpc
INFO[0000] starting containerd                           revision=468a545b9edcd5932818eb9de8e72413e616e86e version=v1.1.2
INFO[0000] loading plugin "io.containerd.content.v1.content"...  type=io.containerd.content.v1
INFO[0000] loading plugin "io.containerd.snapshotter.v1.btrfs"...  type=io.containerd.snapshotter.v1
WARN[0000] failed to load plugin io.containerd.snapshotter.v1.btrfs  error="path /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.btrfs must be a btrfs filesystem to be used with the btrfs snapshotter"
INFO[0000] loading plugin "io.containerd.snapshotter.v1.aufs"...  type=io.containerd.snapshotter.v1
WARN[0000] failed to load plugin io.containerd.snapshotter.v1.aufs  error="modprobe aufs failed: "modprobe: FATAL: Module aufs not found in directory /lib/modules/4.9.0-9-amd64\n": exit status 1"
INFO[0000] loading plugin "io.containerd.snapshotter.v1.native"...  type=io.containerd.snapshotter.v1
INFO[0000] loading plugin "io.containerd.snapshotter.v1.overlayfs"...  type=io.containerd.snapshotter.v1
INFO[0000] loading plugin "io.containerd.snapshotter.v1.zfs"...  type=io.containerd.snapshotter.v1
WARN[0000] failed to load plugin io.containerd.snapshotter.v1.zfs  error="path /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.zfs must be a zfs filesystem to be used with the zfs snapshotter"
INFO[0000] loading plugin "io.containerd.metadata.v1.bolt"...  type=io.containerd.metadata.v1
WARN[0000] could not use snapshotter btrfs in metadata plugin  error="path /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.btrfs must be a btrfs filesystem to be used with the btrfs snapshotter"
WARN[0000] could not use snapshotter aufs in metadata plugin  error="modprobe aufs failed: "modprobe: FATAL: Module aufs not found in directory /lib/modules/4.9.0-9-amd64\n": exit status 1"
WARN[0000] could not use snapshotter zfs in metadata plugin  error="path /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.zfs must be a zfs filesystem to be used with the zfs snapshotter"
WARN[2019-05-27T07:12:30.181008942Z] grpc: addrConn.createTransport failed to connect to {unix:///var/run/docker/containerd/docker-containerd.sock 0  <nil>}. Err :connection error: desc = "transport: error while dialing: dial unix:///var/run/docker/containerd/docker-containerd.sock: timeout". Reconnecting...  module=grpc
INFO[2019-05-27T07:12:30.181072660Z] pickfirstBalancer: HandleSubConnStateChange: 0xc4203605a0, TRANSIENT_FAILURE  module=grpc
INFO[2019-05-27T07:12:30.181164753Z] pickfirstBalancer: HandleSubConnStateChange: 0xc4203605a0, CONNECTING  module=grpc
WARN[2019-05-27T07:12:50.181295638Z] grpc: addrConn.createTransport failed to connect to {unix:///var/run/docker/containerd/docker-containerd.sock 0  <nil>}. Err :connection error: desc = "transport: error while dialing: dial unix:///var/run/docker/containerd/docker-containerd.sock: timeout". Reconnecting...  module=grpc
INFO[2019-05-27T07:12:50.181357013Z] pickfirstBalancer: HandleSubConnStateChange: 0xc4203605a0, TRANSIENT_FAILURE  module=grpc
INFO[2019-05-27T07:12:50.181436917Z] pickfirstBalancer: HandleSubConnStateChange: 0xc4203605a0, CONNECTING  module=grpc
WARN[2019-05-27T07:13:10.181542864Z] Failed to dial unix:///var/run/docker/containerd/docker-containerd.sock: grpc: the connection is closing; please retry.  module=grpc
WARN[2019-05-27T07:13:25.182499550Z] daemon didn't stop within 15 secs, killing it  module=libcontainerd pid=29903
Failed to connect to containerd: failed to dial "/var/run/docker/containerd/docker-containerd.sock": context deadline exceeded
```

it seems i have to reboot the machine

after reboot, all nodes ready now...

```bash
➜  Notes git:(master) kubectl get nodes
NAME                            STATUS   ROLES    AGE     VERSION
ip-172-20-35-247.ec2.internal   Ready    node     10d     v1.12.7
ip-172-20-38-207.ec2.internal   Ready    node     4d22h   v1.12.7
ip-172-20-57-215.ec2.internal   Ready    master   10d     v1.12.7
ip-172-20-63-39.ec2.internal    Ready    node     10d     v1.12.7
```

```bash
➜  Notes git:(master) ✗ kubectl describe node ip-172-20-63-39.ec2.internal
Conditions:
  Type                 Status    LastHeartbeatTime                 LastTransitionTime                Reason                    Message
  ----                 ------    -----------------                 ------------------                ------                    -------
  NetworkUnavailable   False     Fri, 17 May 2019 12:22:01 +0800   Fri, 17 May 2019 12:22:01 +0800   RouteCreated              RouteController created a route
  OutOfDisk            Unknown   Mon, 27 May 2019 16:27:01 +0800   Mon, 27 May 2019 16:27:01 +0800   NodeStatusUnknown         Kubelet stopped posting node status.
  MemoryPressure       Unknown   Mon, 27 May 2019 16:27:01 +0800   Mon, 27 May 2019 16:27:01 +0800   NodeStatusUnknown         Kubelet stopped posting node status.
  DiskPressure         Unknown   Mon, 27 May 2019 16:27:01 +0800   Mon, 27 May 2019 16:27:01 +0800   NodeStatusUnknown         Kubelet stopped posting node status.
  PIDPressure          False     Mon, 27 May 2019 16:27:01 +0800   Fri, 17 May 2019 12:21:58 +0800   KubeletHasSufficientPID   kubelet has sufficient PID available
  Ready                False     Mon, 27 May 2019 16:27:01 +0800   Mon, 27 May 2019 16:27:01 +0800   KubeletNotReady           container runtime is down

Non-terminated Pods:         (28 in total)
  Namespace                  Name                                              CPU Requests  CPU Limits  Memory Requests  Memory Limits  AGE
  ---------                  ----                                              ------------  ----------  ---------------  -------------  ---
  default                    prometheus-operator-6c6646577b-546dt              100m (5%)     200m (10%)  100Mi (5%)       200Mi (10%)    3d3h
  kube-system                kube-dns-57dd96bb49-9554w                         260m (13%)    0 (0%)      110Mi (5%)       170Mi (9%)     3d3h
  kube-system                kube-dns-57dd96bb49-9q9mm                         260m (13%)    0 (0%)      110Mi (5%)       170Mi (9%)     3d3h
  kube-system                kube-dns-autoscaler-867b9fd49d-4fjbm              20m (1%)      0 (0%)      10Mi (0%)        0 (0%)         3d3h
  kube-system                kube-proxy-ip-172-20-63-39.ec2.internal           100m (5%)     0 (0%)      0 (0%)           0 (0%)         3d16h
  kube-system                metrics-server-544fffcc94-sv46k                   0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  kube-system                tiller-deploy-58d57fd669-xsg9c                    0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  monitoring                 alertmanager-main-0                               100m (5%)     100m (5%)   225Mi (12%)      25Mi (1%)      3d3h
  monitoring                 alertmanager-main-1                               100m (5%)     100m (5%)   225Mi (12%)      25Mi (1%)      3d3h
  monitoring                 alertmanager-main-2                               100m (5%)     100m (5%)   225Mi (12%)      25Mi (1%)      3d16h
  monitoring                 grafana-6f7df4bc94-zz8lc                          100m (5%)     200m (10%)  100Mi (5%)       200Mi (10%)    3d3h
  monitoring                 node-exporter-9gjz9                               112m (5%)     270m (13%)  200Mi (10%)      220Mi (11%)    10d
  monitoring                 prometheus-adapter-5ff449fb5c-st5s8               0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  monitoring                 prometheus-k8s-1                                  200m (10%)    200m (10%)  450Mi (24%)      50Mi (2%)      3d16h
  monitoring                 prometheus-operator-88fcf6d95-pdm8b               100m (5%)     200m (10%)  100Mi (5%)       200Mi (10%)    3d3h
  rook-ceph                  maudlin-wallaby-redis-ha-server-1                 0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d16h
  rook-ceph                  mysql-5bc4f5b94b-lcxt2                            0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  rook-ceph                  nginx-ingress-controller-8655977f94-cd6h8         0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  rook-ceph                  nginx-ingress-default-backend-6694789b87-qc5px    0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  rook-ceph                  roiling-mouse-mongodb-55575d8586-t5v5x            0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  rook-ceph                  rook-ceph-agent-9gp7l                             0 (0%)        0 (0%)      0 (0%)           0 (0%)         7d4h
  rook-ceph                  rook-ceph-mgr-a-7954598d69-j6cwz                  0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  rook-ceph                  rook-ceph-mon-c-dbb9d7f5d-ms8vl                   0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d16h
  rook-ceph                  rook-ceph-operator-5d495fcb75-kvps9               0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  rook-ceph                  rook-ceph-osd-1-58456c9875-swb2b                  0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d16h
  rook-ceph                  rook-ceph-rgw-my-store-5ddc4784cc-vpnql           0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  rook-ceph                  rook-ceph-tools-689646bb64-j7kp6                  0 (0%)        0 (0%)      0 (0%)           0 (0%)         3d3h
  rook-ceph                  rook-discover-v992w                               0 (0%)        0 (0%)      0 (0%)           0 (0%)         7d4h
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource                    Requests      Limits
  --------                    --------      ------
  cpu                         1552m (77%)   1370m (68%)
  memory                      1855Mi (99%)  1285Mi (68%)
  ephemeral-storage           0 (0%)        0 (0%)
  attachable-volumes-aws-ebs  0             0
Events:
  Type    Reason        Age                  From                                   Message
  ----    ------        ----                 ----                                   -------
  Normal  NodeNotReady  27s (x7 over 4d21h)  kubelet, ip-172-20-63-39.ec2.internal  Node ip-172-20-63-39.ec2.internal status is now: NodeNotReady
```

memery is not enough... (overcommitted?)

> [resource-requests-and-limits](https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-resource-requests-and-limits)
>
> [kubernetes-container-resource-requirements](https://medium.com/hotels-com-technology/kubernetes-container-resource-requirements-part-1-memory-a9fbe02c8a5f)
>
> [I think the "correct" fix for me is to reduce the number of revisions that Helm stores in configmaps, as other pods that also read all CMs are also hitting their memory limits...](https://github.com/coreos/prometheus-operator/issues/2372)
