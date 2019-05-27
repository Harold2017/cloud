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
```
