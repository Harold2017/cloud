#

## Ingress

> https://kubernetes.io/docs/concepts/services-networking/ingress/

An API object that manages external access to the services in a cluster, typically HTTP. Ingress can provide load blancing, SSL termination and name-based virtual hosting.

* k8s networking

> https://kubernetes.io/docs/concepts/cluster-administration/networking/
>
> * pods on a node can communicate with all pods on all nodes without NAT
>
> * agents on a node (e.g. system daemons, kubelet) can communicate with all pods on that node
>
> Note: For those platforms that support Pods running in the host network (e.g. Linux):
>
> * pods in the host network of a node can communicate with all pods on all nodes without NAT
>
> Kubernetes IP addresses exist at the `Pod` scope - containers within a `Pod` share their network namespaces - including their IP address. This means that containers within a Pod can all reach each other’s ports on `localhost`. This also means that containers within a `Pod` must coordinate port usage, but this is no different from processes in a VM. This is called the “IP-per-pod” model.



* k8s services

> https://kubernetes.io/docs/concepts/services-networking/service/
>
> A Kubernetes `Service` is an abstraction which defines a logical set of `Pods` and a policy by which to access them - sometimes called a micro-service. The set of `Pods` targeted by a `Service` is (usually) determined by a [Label Selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors).

[ingress api group will be changed](https://github.com/kubernetes/enhancements/blob/master/keps/sig-network/20190125-ingress-api-group.md)
