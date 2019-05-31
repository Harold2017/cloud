#

## install with helm

```bash
# add incubator repo
➜  cloud git:(master) ✗ helm repo add incubator https://kubernetes-charts-incubator.storage.googleapis.com/
"incubator" has been added to your repositories

# depoly gogs
➜  cloud git:(master) ✗ helm install --name cicd -f gogs_values.yaml incubator/gogs --namespace cicd
NOTES:
1. Get the Gogs URL by running:

  export NODE_PORT=$(kubectl get --namespace cicd -o jsonpath="{.spec.ports[0].nodePort}" services cicd-gogs)
  export NODE_IP=$(kubectl get nodes --namespace cicd -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT/

2. Register a user.  The first user registered will be the administrator.

➜  cloud git:(master) ✗ kubectl get svc 
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                     AGE
cicd-gogs         NodePort    10.104.152.148   <none>        80:30330/TCP,22:30031/TCP   4m18s
cicd-postgresql   ClusterIP   10.98.112.119    <none>        5432/TCP                    4m18s

➜  cloud git:(master) ✗ kubectl port-forward svc/cicd-gogs 5000:80

# adminA: admin

```