#

## dashboard

> https://github.com/kubernetes/dashboard

* deploy dashboard
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml`

* access dashboard from local workstation by creating a secure channel
`kubectl proxy`

* access dashboard
[link](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/)

## create an authentication token (rbac)

> https://github.com/kubernetes/dashboard/wiki/Creating-sample-user
>
> https://stackoverflow.com/questions/46664104/how-to-sign-in-kubernetes-dashboard

`kubectl config set-credentials cluster-admin --token=bearer_token`

`kubectl -n kube-system describe secret`

`kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')`

`kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | awk '/^deployment-controller-token-/{print $1}') | awk '$1=="token:"{print $2}'`
