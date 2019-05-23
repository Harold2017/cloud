#

## init

> https://helm.sh/docs/using_helm/#installing-helm
> https://helm.sh/docs/using_helm/#quickstart-guide

- install helm on local machine
- run `helm init`
- see whether `tiller` is installed on cluster

    ```bash
    tiller-deploy-5cf8586c77-znvgc     1/1     Running   0      17m
    ```

- get following error when call `helm list`

    ```bash
    ➜  Rook git:(master) ✗ helm list
    Error: configmaps is forbidden: User "system:serviceaccount:kube-system:default" cannot list resource "configmaps" in API group "" in the namespace "kube-system"
    ```

- find this [solution](https://github.com/helm/helm/issues/3130)

> That's because you don't have the permission to deploy tiller, add an account for it:
>
> `kubectl --namespace kube-system create serviceaccount tiller`
>
> `kubectl create clusterrolebinding tiller-cluster-rule \
 --clusterrole=cluster-admin --serviceaccount=kube-system:tiller`
>
> `kubectl --namespace kube-system patch deploy tiller-deploy \
 -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'`
>
> Console output:
>
> serviceaccount "tiller" created
> clusterrolebinding "tiller-cluster-rule" created
> deployment "tiller-deploy" patched

- deploy redis-cluster (1 master, 2 slaves) [redis-ha](https://github.com/helm/charts/tree/master/stable/redis-ha)

    ```bash
    ➜  Rook git:(master) ✗ helm list
    NAME            REVISION        UPDATED                         STATUS          CHART                   APP VERSION     NAMESPACE
    maudlin-wallaby 1               Thu May 23 15:42:13 2019        DEPLOYED        redis-ha-3.4.2          5.0.3           rook-ceph
    nginx-ingress   1               Thu May 23 15:34:27 2019        DEPLOYED        nginx-ingress-1.6.13    0.24.1          rook-ceph

    ➜  Rook git:(master) ✗ kubectl get pods
    NAME                                                        READY   STATUS      RESTARTS   AGE
    maudlin-wallaby-redis-ha-server-0                           2/2     Running     0          2m28s
    maudlin-wallaby-redis-ha-server-1                           2/2     Running     0          103s
    maudlin-wallaby-redis-ha-server-2                           2/2     Running     0          56s
    ```

- helm is awesome!
