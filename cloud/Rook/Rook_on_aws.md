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