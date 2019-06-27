#

## [gitlab chart](https://docs.gitlab.com/charts/)

[deployment](https://docs.gitlab.com/charts/installation/deployment.html)

[cmd options](https://docs.gitlab.com/charts/installation/command-line-options.html)

[CE or EE](https://about.gitlab.com/install/ce-or-ee/)

[charts](https://gitlab.com/charts/gitlab)

```bash
➜  cloud git:(master) ✗ helm repo add gitlab https://charts.gitlab.io/
helm repo update
helm upgrade --install gitlab gitlab/gitlab \
  --timeout 600 \
  --set global.hosts.domain=<example.com> \ # not used
  --set global.hosts.externalIP=<master node static ip> \ # not used
  --set certmanager-issuer.email=<my work email>
  --namespace cicd
```

problems:

```bash
➜  cloud git:(master) ✗ kubectl describe pods/gitlab-postgresql-554d9fc6d5-6b926                                     
Name:               gitlab-postgresql-554d9fc6d5-6b926
Namespace:          cicd
Priority:           0
PriorityClassName:  <none>
Node:               <none>
Labels:             app=postgresql
                    pod-template-hash=554d9fc6d5
                    release=gitlab
Annotations:        kubernetes.io/psp: 00-pharos-privileged
Status:             Pending
IP:                 
Controlled By:      ReplicaSet/gitlab-postgresql-554d9fc6d5
Containers:
  gitlab-postgresql:
    Image:      postgres:9.6.8
    Port:       5432/TCP
    Host Port:  0/TCP
    Requests:
      cpu:      100m
      memory:   256Mi
    Liveness:   exec [sh -c exec pg_isready --host $POD_IP] delay=120s timeout=5s period=10s #success=1 #failure=6
    Readiness:  exec [sh -c exec pg_isready --host $POD_IP] delay=5s timeout=3s period=5s #success=1 #failure=3
    Environment:
      POSTGRES_USER:           gitlab
      PGUSER:                  gitlab
      POSTGRES_DB:             gitlabhq_production
      POSTGRES_INITDB_ARGS:    
      PGDATA:                  /var/lib/postgresql/data/pgdata
      POSTGRES_PASSWORD_FILE:  /conf/postgres-password
      POD_IP:                   (v1:status.podIP)
    Mounts:
      /conf from password-file (ro)
      /var/lib/postgresql/data/pgdata from data (rw,path="postgresql-db")
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-fjhrs (ro)
  metrics:
    Image:      wrouesnel/postgres_exporter:v0.1.1
    Port:       9187/TCP
    Host Port:  0/TCP
    Requests:
      cpu:     100m
      memory:  256Mi
    Environment:
      DATA_SOURCE_NAME:  postgresql://gitlab@127.0.0.1:5432?sslmode=disable
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-fjhrs (ro)
Conditions:
  Type           Status
  PodScheduled   False 
Volumes:
  data:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  gitlab-postgresql
    ReadOnly:   false
  password-file:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  gitlab-postgresql-password
    Optional:    false
  default-token-fjhrs:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-fjhrs
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason            Age                  From               Message
  ----     ------            ----                 ----               -------
  Warning  FailedScheduling  11s (x5 over 4m14s)  default-scheduler  pod has unbound immediate PersistentVolumeClaims (repeated 3 times)

➜  cloud git:(master) ✗ kubectl get pvc                                         
NAME                        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
gitlab-minio                Pending                                                     4m46s
gitlab-postgresql           Pending                                                     4m46s
gitlab-prometheus-server    Pending                                                     4m46s
gitlab-redis                Pending                                                     4m46s
repo-data-gitlab-gitaly-0   Pending                                                     16m

➜  cloud git:(master) ✗ kubectl describe pvc/gitlab-postgresql
Name:          gitlab-postgresql
Namespace:     cicd
StorageClass:  
Status:        Pending
Volume:        
Labels:        app=postgresql
               chart=postgresql-0.12.0
               heritage=Tiller
               release=gitlab
Annotations:   <none>
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      
Access Modes:  
VolumeMode:    Filesystem
Events:
  Type       Reason         Age                  From                         Message
  ----       ------         ----                 ----                         -------
  Normal     FailedBinding  6s (x23 over 5m19s)  persistentvolume-controller  no persistent volumes available for this claim and no storage class is set
Mounted By:  gitlab-postgresql-554d9fc6d5-6b926
```

## use [gitlab ce chart](https://github.com/helm/charts/tree/master/stable/gitlab-ce) instead

```bash
➜  cloud git:(master) ✗ helm install --name gitlab -f cicd/gitlab_ce_values.yaml stable/gitlab-ce --namespace cicd
...
## WARNING: You did not specify an externalUrl in your 'helm install' call. ##
##############################################################################

This deployment will be incomplete until you provide the URL that your
GitLab install will be reachable to your users under:

    helm upgrade gitlab \
        --set externalUrl=http://your-domain.com stable/gitlab-ce

➜  cloud git:(master) ✗ helm upgrade gitlab \
        --set externalUrl=http://astri.com stable/gitlab-ce
...
1. Get your GitLab URL by running:

  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        Watch the status with: 'kubectl get svc -w gitlab-gitlab-ce'

  export SERVICE_IP=$(kubectl get svc --namespace cicd gitlab-gitlab-ce -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  echo http://$SERVICE_IP/

2. Set your admin user's password on your first visit to your install. Then
   login as:

   Username: root
   Password: <whatever value you entered>

3. Point a DNS entry at your install to ensure that your specified
   external URL is reachable:

   http://astri.com
```

problems:

```bash
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  31s (x3 over 91s)  default-scheduler  pod has unbound immediate PersistentVolumeClaims (repeated 3 times)
```

[k8s storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
[k8s default storage-class](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#class-1)

problems:

```bash
➜  cloud git:(master) ✗ kubectl describe pvc/gitlab-gitlab-ce-data                 
Name:          gitlab-gitlab-ce-data
Namespace:     cicd
StorageClass:  standard
Status:        Pending
Volume:        
Labels:        <none>
Annotations:   volume.beta.kubernetes.io/storage-class: standard
               volume.beta.kubernetes.io/storage-provisioner: kubernetes.io/aws-ebs
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      
Access Modes:  
VolumeMode:    Filesystem
Events:
  Type       Reason              Age                   From                         Message
  ----       ------              ----                  ----                         -------
  Warning    ProvisioningFailed  20s (x10 over 8m20s)  persistentvolume-controller  Failed to provision volume with StorageClass "standard": Failed to get AWS Cloud Provider. GetCloudProvider returned <nil> instead
Mounted By:  gitlab-gitlab-ce-74f54564f4-wj9wm
```

[aws cloud provider](https://blog.scottlowe.org/2018/09/28/setting-up-the-kubernetes-aws-cloud-provider/)
[pharos cloud providers](https://pharos.sh/docs/cloud_providers/)

add cloud provider in `cluster.yaml` and re-config the cluster `pharos up -c cluster.yaml --force`

after this, pharos got stuck at `Configure kube client @ ip-10-0-2-165 [ip-10-0-2-165] Fetching kubectl config`

[rancher cloud provider aws](https://rancher.com/docs/rke/latest/en/config-options/cloud-providers/aws/)
[tag ec2 resources](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html)
[k8s on aws](https://medium.com/jane-ai-engineering-blog/kubernetes-on-aws-6281e3a830fe)

this stuck is due to master node problem... re-launch another node and it suck as the following:

```bash
Configure master @ ip-10-0-2-67
    [ip-10-0-2-67] Checking if Kubernetes control plane is already initialized ...
    [ip-10-0-2-67] Kubernetes control plane is not initialized.
    [ip-10-0-2-67] Initializing control plane (v1.14.3) ...
    [ip-10-0-2-67] Retrying after 2 seconds (#1) ...
    [ip-10-0-2-67] Checking if Kubernetes control plane is already initialized ...
    [ip-10-0-2-67] Renewing control plane certificates ...
    [ip-10-0-2-67] Reconfiguring control plane (v1.14.3)..
```

setup a new iam role and attach it to all nodes, and add same tags to nodes, subnets, security groups

Example IAM role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["ec2:*"],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["elasticloadbalancing:*"],
      "Resource": ["*"]
    }
  ]
}
```

<CLUSTER_ID> is the `name` in `cluster.yaml`

Tag syntax:

- key = kubernetes.io/cluster/<CLUSTER_ID>
- value = shared

Now, the cluster is successfully launched!

```bash
➜  cloud git:(master) ✗ kubectl describe pods/kubelet-rubber-stamp-7bcb5876d5-z666f                                     
Name:               kubelet-rubber-stamp-7bcb5876d5-z666f
Namespace:          kube-system
Priority:           2000000000
PriorityClassName:  system-cluster-critical
Node:               ip-10-0-0-75.ec2.internal/10.0.0.75
Start Time:         Thu, 27 Jun 2019 17:05:47 +0800
Labels:             name=kubelet-rubber-stamp
                    pod-template-hash=7bcb5876d5
Annotations:        kubernetes.io/psp: 00-pharos-privileged
Status:             Pending
IP:                 
Controlled By:      ReplicaSet/kubelet-rubber-stamp-7bcb5876d5
Containers:
  rubber-stamp:
    Container ID:   
    Image:          registry.pharos.sh/kontenapharos/kubelet-rubber-stamp:0.1.0
    Image ID:       
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       ContainerCreating
    Ready:          False
    Restart Count:  0
    Environment:
      WATCH_NAMESPACE:  
      POD_NAME:         kubelet-rubber-stamp-7bcb5876d5-z666f (v1:metadata.name)
      OPERATOR_NAME:    kubelet-rubber-stamp
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kubelet-rubber-stamp-token-bdhlf (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  kubelet-rubber-stamp-token-bdhlf:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kubelet-rubber-stamp-token-bdhlf
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  node-role.kubernetes.io/master=
Tolerations:     :NoSchedule
                 node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason                  Age                    From                                Message
  ----     ------                  ----                   ----                                -------
  Normal   Scheduled               4m13s                  default-scheduler                   Successfully assigned kube-system/kubelet-rubber-stamp-7bcb5876d5-z666f to ip-10-0-0-75.ec2.internal
  Warning  FailedCreatePodSandBox  4m11s                  kubelet, ip-10-0-0-75.ec2.internal  Failed create pod sandbox: rpc error: code = Unknown desc = [failed to set up sandbox container "49268b5153ffc6ccadceabaa287402e4684a4b713b8db547029bdf6d92e015ca" network for pod "kubelet-rubber-stamp-7bcb5876d5-z666f": NetworkPlugin cni failed to set up pod "kubelet-rubber-stamp-7bcb5876d5-z666f_kube-system" network: failed to find plugin "weave-net" in path [/opt/cni/bin], failed to clean up sandbox container "49268b5153ffc6ccadceabaa287402e4684a4b713b8db547029bdf6d92e015ca" network for pod "kubelet-rubber-stamp-7bcb5876d5-z666f": NetworkPlugin cni failed to teardown pod "kubelet-rubber-stamp-7bcb5876d5-z666f_kube-system" network: failed to find plugin "weave-net" in path [/opt/cni/bin]]
  Normal   SandboxChanged          3m55s (x2 over 4m11s)  kubelet, ip-10-0-0-75.ec2.internal  Pod sandbox changed, it will be killed and re-created.
  Warning  FailedCreatePodSandBox  89s                  kubelet, ip-10-0-0-75.ec2.internal  Failed create pod sandbox: rpc error: code = DeadlineExceeded desc = context deadline exceeded

➜  cloud git:(master) ✗ kubectl describe pods/coredns-6f95d85ccd-ztgwb             
Name:               coredns-6f95d85ccd-ztgwb
Namespace:          kube-system
Priority:           2000000000
PriorityClassName:  system-cluster-critical
Node:               ip-10-0-0-75.ec2.internal/10.0.0.75
Start Time:         Thu, 27 Jun 2019 17:05:55 +0800
Labels:             k8s-app=kube-dns
                    pod-template-hash=6f95d85ccd
Annotations:        kubernetes.io/psp: 00-pharos-privileged
Status:             Pending
IP:                 
Controlled By:      ReplicaSet/coredns-6f95d85ccd
Containers:
  coredns:
    Container ID:  
    Image:         registry.pharos.sh/kontenapharos/coredns:1.3.1
    Image ID:      
    Ports:         53/UDP, 53/TCP, 9153/TCP
    Host Ports:    0/UDP, 0/TCP, 0/TCP
    Args:
      -conf
      /etc/coredns/Corefile
    State:          Waiting
      Reason:       ContainerCreating
    Ready:          False
    Restart Count:  0
    Limits:
      memory:  170Mi
    Requests:
      cpu:        100m
      memory:     70Mi
    Liveness:     http-get http://:8080/health delay=60s timeout=5s period=10s #success=1 #failure=5
    Readiness:    http-get http://:8080/health delay=0s timeout=1s period=10s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /etc/coredns from config-volume (ro)
      /var/run/secrets/kubernetes.io/serviceaccount from coredns-token-ct74k (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  config-volume:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      coredns
    Optional:  false
  coredns-token-ct74k:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  coredns-token-ct74k
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  beta.kubernetes.io/os=linux
Tolerations:     CriticalAddonsOnly
                 node-role.kubernetes.io/master:NoSchedule
                 node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason                  Age                    From                                Message
  ----     ------                  ----                   ----                                -------
  Warning  FailedScheduling        6m35s (x5 over 7m9s)   default-scheduler                   0/1 nodes are available: 1 node(s) had taints that the pod didn't tolerate.
  Warning  FailedScheduling        6m30s (x2 over 6m31s)  default-scheduler                   0/2 nodes are available: 2 node(s) had taints that the pod didn't tolerate.
  Normal   Scheduled               6m26s                  default-scheduler                   Successfully assigned kube-system/coredns-6f95d85ccd-ztgwb to ip-10-0-0-75.ec2.internal
  Warning  FailedCreatePodSandBox  2m26s                  kubelet, ip-10-0-0-75.ec2.internal  Failed create pod sandbox: rpc error: code = DeadlineExceeded desc = context deadline exceeded
  Normal   SandboxChanged          2m25s                  kubelet, ip-10-0-0-75.ec2.internal  Pod sandbox changed, it will be killed and re-created.
```

re-edit `cluster.yml` and re-edit `IAM role`, re-create clusters

same problem occurred...

follow [this](https://github.com/kubernetes/kubernetes/issues/48798#issuecomment-452172710)

```bash
➜  cloud git:(master) ✗ kubectl describe pods/coredns-6f95d85ccd-2kbqq
...
Events:
  Type     Reason     Age                  From                                Message
  ----     ------     ----                 ----                                -------
  Normal   Scheduled  2m44s                default-scheduler                   Successfully assigned kube-system/coredns-6f95d85ccd-2kbqq to ip-10-0-0-46.ec2.internal
  Normal   Pulled     89s (x3 over 2m41s)  kubelet, ip-10-0-0-46.ec2.internal  Successfully pulled image "registry.pharos.sh/kontenapharos/coredns:1.3.1"
  Normal   Created    89s (x3 over 2m41s)  kubelet, ip-10-0-0-46.ec2.internal  Created container coredns
  Normal   Started    89s (x3 over 2m41s)  kubelet, ip-10-0-0-46.ec2.internal  Started container coredns
  Warning  Unhealthy  59s (x9 over 2m39s)  kubelet, ip-10-0-0-46.ec2.internal  Readiness probe failed: HTTP probe failed with statuscode: 503
  Warning  BackOff    50s (x3 over 99s)    kubelet, ip-10-0-0-46.ec2.internal  Back-off restarting failed container
  Normal   Pulling    37s (x4 over 2m43s)  kubelet, ip-10-0-0-46.ec2.internal  Pulling image "registry.pharos.sh/kontenapharos/coredns:1.3.1

➜  cloud git:(master) ✗ kubectl get pods                               
NAME                                                 READY   STATUS              RESTARTS   AGE
coredns-6f95d85ccd-2kbqq                             0/1     CrashLoopBackOff    5          6m24s
coredns-6f95d85ccd-6gcp4                             0/1     CrashLoopBackOff    5          6m39s
```

```bash
➜  cloud git:(master) ✗ kubectl describe pods/kubelet-rubber-stamp-7bcb5876d5-npmnw              ...
Events:
  Type     Reason                  Age                 From                                 Message
  ----     ------                  ----                ----                                 -------
  Normal   Scheduled               32m                 default-scheduler                    Successfully assigned kube-system/kubelet-rubber-stamp-7bcb5876d5-npmnw to ip-10-0-0-139.ec2.internal
  Warning  FailedCreatePodSandBox  32m                 kubelet, ip-10-0-0-139.ec2.internal  Failed create pod sandbox: rpc error: code = Unknown desc = [failed to set up sandbox container "9e738f41b3945c2d171a00797503c0cf499ca6b7b58edf9cb7c46cea41d56f6d" network for pod "kubelet-rubber-stamp-7bcb5876d5-npmnw": NetworkPlugin cni failed to set up pod "kubelet-rubber-stamp-7bcb5876d5-npmnw_kube-system" network: failed to find plugin "weave-net" in path [/opt/cni/bin], failed to clean up sandbox container "9e738f41b3945c2d171a00797503c0cf499ca6b7b58edf9cb7c46cea41d56f6d" network for pod "kubelet-rubber-stamp-7bcb5876d5-npmnw": NetworkPlugin cni failed to teardown pod "kubelet-rubber-stamp-7bcb5876d5-npmnw_kube-system" network: failed to find plugin "weave-net" in path [/opt/cni/bin]]
  Normal   SandboxChanged          35s (x10 over 32m)  kubelet, ip-10-0-0-139.ec2.internal  Pod sandbox changed, it will be killed and re-created.
  Warning  FailedCreatePodSandBox  35s (x8 over 28m)   kubelet, ip-10-0-0-139.ec2.internal  Failed create pod sandbox: rpc error: code = DeadlineExceeded desc = context deadline exceeded
  Warning  FailedMount             25s                   kubelet, ip-10-0-0-139.ec2.internal  MountVolume.SetUp failed for volume "kubelet-rubber-stamp-token-ts8rw" : couldn't propagate object cache: timed out waiting for the condition
  Normal   SandboxChanged          24s                   kubelet, ip-10-0-0-139.ec2.internal  Pod sandbox changed, it will be killed and re-created.
```

## use kops

now everything works well...

```bash

1. Get your GitLab URL by running:

  export NODE_IP=$(kubectl get nodes --namespace cicd -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP/

2. Login as the root user:

  Username: root
  Password: gitlab


3. Point a DNS entry at your install to ensure that your specified
   external URL is reachable:

   http://astri.com/

➜  cicd git:(master) ✗ export NODE_IP=$(kubectl get nodes --namespace cicd -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP/
http://172.20.38.77/

➜  cicd git:(master) ✗ kubectl get pods
NAME                                 READY   STATUS    RESTARTS   AGE
gitlab-gitlab-ce-69dcb69f6c-vg6j4    1/1     Running   1          3m25s
gitlab-postgresql-765ff48f59-lrgmw   1/1     Running   0          3m25s
gitlab-redis-7574c9c494-mlz5b        1/1     Running   0          3m25s
```

```bash
➜  cicd git:(master) ✗ helm install --name drone stable/drone -f drone_gitlab_values.yaml --namespace cicd

➜  cicd git:(master) ✗ kubectl create secret generic drone-server-secrets \
      --namespace=cicd \
      --from-literal=clientSecret="0ad9011216a997b70f1c082ed21045b1a3b60b55454ebde0808934eccdd22aae"
secret/drone-server-secrets created

➜  cicd git:(master) ✗ helm upgrade drone \
      --reuse-values \
      --set 'sourceControl.provider=gitlab' \
      --set 'sourceControl.gitlab.clientID=7a60b75fb1e7c3182ed30766175134963a55144edd846d0b9a5385a2c1f6a993' \
      --set 'sourceControl.secret=drone-server-secrets' \
      --set 'server=http://100.64.30.151:80' \
      stable/drone
...
Get the Drone URL by running:
  export POD_NAME=$(kubectl get pods -n cicd -l "component=server,app=drone,release=drone" -o jsonpath="{.items[0].metadata.name}")
  echo http://127.0.0.1:8000/
  kubectl -n cicd port-forward $POD_NAME 8000:80
```

`Failed to load resource: the server responded with a status of 401 (Unauthorized)`
