#

## deploy drone with helm

```bash
➜  cloud git:(master) ✗ helm install --name drone stable/drone --namespace cicd
NOTES:
##############################################################################
####        ERROR: You did not set a valid version control provider       ####
##############################################################################

This deployment will be incomplete until you configure a valid version
control provider:

    kubectl create secret generic drone-server-secrets \
      --namespace=cicd \
      --from-literal=clientSecret="github-oauth2-client-secret"

    helm upgrade drone \
      --reuse-values \
      --set 'sourceControl.provider=github' \
      --set 'sourceControl.github.clientID=github-oauth2-client-id' \
      --set 'sourceControl.secret=drone-server-secrets' \
      stable/drone

Currently supported providers:

    - GitHub
    - GitLab
    - Gitea
    - Gogs
    - Bitbucket Cloud
    - Bitbucket Server (Stash)

See the values.yaml file to see what values are required for each provider.

If you are having trouble with the configuration of a provider please visit
the official documentation:

    http://docs.drone.io/installation/
```

[setup](https://docs.drone.io/installation/gogs/kubernetes/)

```bash
# generate a shared secret to authenticate communication between Pipeline controllers and your central Drone server.
# This shared secret is passed to both the server using the DRONE_RPC_SECRET environment variable.
➜  cloud git:(master) ✗ openssl rand -hex 16
f8a22eed628797f48ff347658fcfff03

# change values.yaml

➜  cloud git:(master) ✗ helm install --name drone -f drone_values.yaml stable/drone --namespace cicd
NOTES:

*********************************************************************************
***        PLEASE BE PATIENT: drone may take a few minutes to install         ***
*********************************************************************************

Get the Drone URL by running:
  export POD_NAME=$(kubectl get pods -n cicd -l "component=server,app=drone,release=drone" -o jsonpath="{.items[0].metadata.name}")
  echo http://127.0.0.1:8000/
  kubectl -n cicd port-forward $POD_NAME 8000:80

# adminA: admin
```

[metrics](https://docs.drone.io/administration/server/metrics/)

```bash
# create a machine user
drone user create prometheus --machine --token=f8a22eed628797f48ff347658fcfff03
```

pending...
