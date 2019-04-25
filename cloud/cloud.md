#

## Prometheus

> https://www.ibm.com/developerworks/cn/cloud/library/cl-lo-prometheus-getting-started-and-practice/index.html
>
> ![Prometheus Architect](https://www.ibm.com/developerworks/cn/cloud/library/cl-lo-prometheus-getting-started-and-practice/image001.png)

## k8s

> https://www.kubernetes.org.cn/course
> https://www.kubernetes.org.cn/4047.html
> ![K8s Architect](https://www.ibm.com/developerworks/cn/cloud/library/cl-lo-devops-via-kubernetes-and-containers/image003.jpg)
>
> ![K8s Architect](https://res.cloudinary.com/dukp6c7f7/image/upload/f_auto,fl_lossy,q_auto/s3-ghost/2016/06/o7leok.png)
>
> ![K8s container runtime](https://www.kubernetes.org.cn/img/2018/05/Image-2016-12-19-at-17.13.16.png)

quick start:
> https://cloud.google.com/kubernetes-engine/docs/quickstart
>
> https://kubernetes.io/docs/tutorials/hello-minikube/
>
> https://kubernetes.io/docs/setup/minikube/

start with minikube

```bash
# install minikube
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/

# install virtualbox
# https://www.virtualbox.org/wiki/Downloads

# install libvirt-bin (https://github.com/kubernetes/minikube/issues/927)
# sudo apt-get install libvert-bin

minikube start

kubectl get nodes
# NAME       STATUS   ROLES    AGE   VERSION
# minikube   Ready    master   84s   v1.14.0

minikube dashboard

# Set docker env
eval $(minikube docker-env)

# build demo docker
docker build -t demo:0.0.0 -f Dockerfile .

# save image
docker save imageNameGoesHere > pv | (eval $(minikube docker-env) && docker load)

# image pulling
# https://kubernetes.io/docs/concepts/containers/images/#updating-images

# create a Deployment that manages a Pod. The Pod runs a Container based on the provided Docker image.
kubectl create deployment demo --image=demo:0.0.0
# deployment.apps/demo created

# view the Deployment
kubectl get deployments
# NAME   READY   UP-TO-DATE   AVAILABLE   AGE
# demo   1/1     1            1           58s

# view the Pod
kubectl get pods
# NAME                    READY   STATUS    RESTARTS   AGE
# demo-7b888bd64c-jtr65   1/1     Running   0          7s

# view cluster events
kubectl get events

# view the kubectl configuration
kubectl config view
: '
apiVersion: v1
clusters:
- cluster:
    certificate-authority: /home/harold/.minikube/ca.crt
    server: https://192.168.99.100:8443
  name: minikube
contexts:
- context:
    cluster: minikube
    user: minikube
  name: minikube
current-context: minikube
kind: Config
preferences: {}
users:
- name: minikube
  user:
    client-certificate: /home/harold/.minikube/client.crt
    client-key: /home/harold/.minikube/client.key
'

# delete deployment
kubectl delete deployment demo

# create a service
## By default, the Pod is only accessible by its internal IP address within the Kubernetes cluster. To make the hello-node Container accessible from outside the Kubernetes virtual network, you have to expose the Pod as a Kubernetes Service.
### expose the Pod to the public internet using the kubectl expose command
kubectl expose deployment demo --type=LoadBalancer --port=8080
# service/demo exposed
### view the service just created
kubectl get services
# NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
# demo         LoadBalancer   10.111.20.81   <pending>     8080:31227/TCP   51s
# kubernetes   ClusterIP      10.96.0.1      <none>        443/TCP          56m

# On Minikube, the LoadBalancer type makes the Service accessible through the minikube service command.
minikube service demo
# see `Hello World!` in auto-open browser

# list currently support addons
minikube addons list

# enable an addon
minikube addons enable xxx

# view the Pod and Service just created
kubectl get pod,svc -n kube-system
# NAME                                        READY   STATUS    RESTARTS   AGE
# pod/coredns-fb8b8dccf-46qrw                 1/1     Running   3          65m
# pod/coredns-fb8b8dccf-76mdr                 1/1     Running   3          65m
# pod/etcd-minikube                           1/1     Running   1          64m
# pod/kube-addon-manager-minikube             1/1     Running   1          63m
# pod/kube-apiserver-minikube                 1/1     Running   2          64m
# pod/kube-controller-manager-minikube        1/1     Running   0          45m
# pod/kube-proxy-rr7rs                        1/1     Running   0          45m
# pod/kube-scheduler-minikube                 1/1     Running   2          64m
# pod/kubernetes-dashboard-79dd6bfc48-qvdmd   1/1     Running   3          63m
# pod/storage-provisioner                     1/1     Running   3          64m


# NAME                           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                  AGE
# service/kube-dns               ClusterIP   10.96.0.10     <none>        53/UDP,53/TCP,9153/TCP   65m
# service/kubernetes-dashboard   ClusterIP   10.102.80.77   <none>        80/TCP                   63m

# disable one addon
minikube addons disable xxx

# clean up
## clean up resources created in the cluster
kubectl delete service demo
kubectl delete deployment demo

## stop the Minikube VM
minikube stop

## delete the Minikube VM
minikube delete
```

### k8s concepts

> https://kubernetes.io/docs/concepts/

## DevOps with k8s

> https://www.ibm.com/developerworks/cn/cloud/library/cl-lo-devops-via-kubernetes-and-containers/index.html
