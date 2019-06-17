#

## OpenFaaS

[link](https://github.com/openfaas/faas)

[OpenFaaS on k8s](https://docs.openfaas.com/deployment/kubernetes/)

[Helm Chart](https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md)

[faas-cli](https://github.com/openfaas/faas-cli)

```bash
# create namespaces
➜  cloud git:(master) kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
# add faas repo
➜  cloud git:(master) helm repo add openfaas https://openfaas.github.io/faas-netes/
"openfaas" has been added to your repositories

# generate secrets to enable basic authentication
# generate a random password
➜  cloud git:(master) PASSWORD=$(head -c 12 /dev/urandom | shasum| cut -d' ' -f1)
➜  cloud git:(master) echo $PASSWORD
f99883697dac5606416c112400b85351f82d2a1e
# create secrets
➜  cloud git:(master) kubectl -n openfaas create secret generic basic-auth \
--from-literal=basic-auth-user=admin \
--from-literal=basic-auth-password="$PASSWORD"
secret/basic-auth created
# install openfaas
➜  cloud git:(master) helm repo update \       
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set basic_auth=true \
    --set functionNamespace=openfaas-fn \
    --set ingress.enabled=true
# check installation
➜  cloud git:(master) kubectl get svc -n openfaas gateway-external -o wide
NAME               TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE   SELECTOR
gateway-external   NodePort   10.99.66.62   <none>        8080:31112/TCP   44m   app=gateway
# port forward
➜  cloud git:(master) kubectl port-forward -n openfaas svc/gateway 3000:8080 &
[1] 3717
➜  cloud git:(master) Forwarding from 127.0.0.1:3000 -> 8080
Forwarding from [::1]:3000 -> 8080

# install faas-cli
➜  cloud git:(master) curl -sSL https://cli.openfaas.com | sudo sh
# login with CLI
export OPENFAAS_URL=http://127.0.0.1:3000
echo -n $PASSWORD | faas-cli login -g $OPENFAAS_URL -u admin --password-stdin
# check
➜  cloud git:(master) faas-cli version
  ___                   _____           ____
 / _ \ _ __   ___ _ __ |  ___|_ _  __ _/ ___|
| | | | '_ \ / _ \ '_ \| |_ / _` |/ _` \___ \
| |_| | |_) |  __/ | | |  _| (_| | (_| |___) |
 \___/| .__/ \___|_| |_|_|  \__,_|\__,_|____/
      |_|

CLI:
 commit:  25cada08609e00bed526790a6bdd19e49ca9aa63
 version: 0.8.14
Handling connection for 3000

# delete
helm delete --purge openfaas
kubectl delete namespace openfaas openfaas-fn

# metrics
➜  cloud git:(master) ✗ kubectl get svc -n openfaas prometheus -o wide 
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE   SELECTOR
prometheus   ClusterIP   10.110.164.95   <none>        9090/TCP   92m   app=prometheus
# set grafana dashboard
# data source: http://10.110.164.95:9090
```

[zero scale](https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md#zero-scale)

[configuration parameters](https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md#configuration)

```bash
# deploy demo function
faas-cli -action deploy -image=faasandfurious/qrcode -name=qrcode -fprocess="/usr/bin/qrcode"
200 OK
http://localhost:3000/function/qrcode-go
# check
➜  cloud git:(master) kubectl get pods -n openfaas-fn  
NAME                         READY   STATUS    RESTARTS   AGE
qrcode-go-597f4c7b94-djtnl   1/1     Running   0          3m4s
# test
➜  cloud git:(master) ✗ curl localhost:3000/function/qrcode-go --data "https://github.com/alexellis/faas" > qrcode.png
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0Handling connection for 3000
100   674  100   641  100    33    986     50 --:--:-- --:--:-- --:--:--  1035
```

[python function](https://blog.alexellis.io/first-faas-python-function/)

```bash
# create a new python function with CLI
➜  functions git:(master) ✗ faas-cli new --lang python hello-python
# change gateway in hello-python.yml
➜  cloud git:(master) ✗ kubectl get svc -n openfaas gateway -o wideNAME      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE    SELECTOR
gateway   ClusterIP   10.106.79.236   <none>        8080/TCP   101m   app=gateway
# build the function
faas-cli build -f ./hello-python.yml
# check the built image
➜  cloud git:(master) ✗ docker images | grep hello-python
hello-python                         latest              06764d6e748e        About a minute ago   75.1MB
# upload the image to docker hub
# docker tag local-image:tagname new-repo:tagname
# docker push new-repo:tagname
# docker login
➜  cloud git:(master) ✗ docker tag hello-python:latest harold2017/hello-python:latest
➜  cloud git:(master) ✗ docker push harold2017/hello-python:latest
The push refers to repository [docker.io/harold2017/hello-python]
# log in faas-cli
➜  cloud git:(master) ✗ kubectl port-forward -n openfaas svc/gateway 3000:8080 &
➜  cloud git:(master) ✗ faas-cli login --password=f99883697dac5606416c112400b85351f82d2a1e
# push function to openfaas
➜  cloud git:(master) ✗ faas-cli push -f openfaas/functions/hello-python.yml
# deploy the function
➜  cloud git:(master) ✗ faas-cli deploy -f openfaas/functions/hello-python.yml
Deploying: hello-python.
WARNING! Communication is not secure, please consider using HTTPS. Letsencrypt.org offers free SSL/TLS certificates.
Handling connection for 3000
Handling connection for 3000

Deployed. 202 Accepted.
URL: http://localhost:3000/function/hello-python

# test with curl
➜  cloud git:(master) ✗ curl http://localhost:3000/function/hello-python -d "harold"
➜  cloud git:(master) ✗ faas-cli list
Handling connection for 3000
Function                        Invocations     Replicas
hello-python                    4               1    
qrcode-go                       3               1  

```

[troubleshooting](https://docs.openfaas.com/deployment/troubleshooting/)

```bash
# change the handler.py with 3rd party lib
# add lib in requirements.txt
# rebuild:
➜  cloud git:(master) ✗ faas-cli build -f openfaas/functions/hello-python.yml
# re-push:
➜  cloud git:(master) ✗ faas-cli push -f openfaas/functions/hello-python.yml
# re-deploy
➜  cloud git:(master) ✗ faas-cli deploy -f openfaas/functions/hello-python.yml
# re-test
➜  cloud git:(master) ✗ curl localhost:3000/function/hello-python --data-binary '{
 "url": "https://blog.alexellis.io/rss/",
 "term": "docker"
}'
Handling connection for 3000
{"found": true}
```
