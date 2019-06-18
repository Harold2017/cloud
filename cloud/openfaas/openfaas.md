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

```bash
# pre-set-env
➜  cloud git:(master) export PASSWORD=f99883697dac5606416c112400b85351f82d2a1e
➜  cloud git:(master) export OPENFAAS_URL=http://127.0.0.1:3000
➜  cloud git:(master) export KUBECONFIG=./kubeconfig
➜  cloud git:(master) ✗ kubectl port-forward -n openfaas svc/gateway 3000:8080 &
```

### Ingress

```bash
➜  cloud git:(master) ✗ kubectl get ingress --all-namespaces
NAMESPACE   NAME                                      HOSTS                    ADDRESS   PORTS   AGE
openfaas    openfaas-gateway-ingress                  *                                  80      14m
openfaas    openfaas-ingress                          gateway.openfaas.local             80      19h
rook-ceph   rook-ceph-rgw-my-store-external-ingress   *                                  80      6d23h

➜  cloud git:(master) ✗ kubectl describe ingress openfaas-gateway-ingress -n openfaas
Name:             openfaas-gateway-ingress
Namespace:        openfaas
Address:
Default backend:  default-http-backend:80 (<none>)
Rules:
  Host  Path  Backends
  ----  ----  --------
  *
        /openfaas   gateway:8080 (10.32.0.9:8080)
Annotations:
  kubectl.kubernetes.io/last-applied-configuration:  {"apiVersion":"extensions/v1beta1","kind":"Ingress","metadata":{"annotations":{"kubernetes.io/ingress.class":"nginx"},"name":"openfaas-gateway-ingress","namespace":"openfaas"},"spec":{"rules":[{"http":{"paths":[{"backend":{"serviceName":"gateway","servicePort":8080},"path":"/openfaas"}]}}]}}

  kubernetes.io/ingress.class:  nginx
Events:
  Type    Reason  Age   From                      Message
  ----    ------  ----  ----                      -------
  Normal  CREATE  19m   nginx-ingress-controller  Ingress openfaas/openfaas-gateway-ingress

# can NOT login...
➜  cloud git:(master) ✗ faas-cli login --gateway https://xxx.compute-1.amazonaws.com/openfaas --password=f99883697dac5606416c112400b85351f82d2a1e
WARNING! Using --password is insecure, consider using: cat ~/faas_pass.txt | faas-cli login -u user --password-stdin
Calling the OpenFaaS server to validate the credentials...
Cannot connect to OpenFaaS on URL: https://xxx.compute-1.amazonaws.com/openfaas. Get https://xxx.compute-1.amazonaws.com/openfaas/system/functions: x509: certificate is valid for ingress.local, not xxx.compute-1.amazonaws.com

➜  cloud git:(master) ✗ faas-cli login --gateway https://<public-ip>/openfaas --password=f99883697dac5606416c112400b85351f82d2a1e
WARNING! Using --password is insecure, consider using: cat ~/faas_pass.txt | faas-cli login -u user --password-stdin
Calling the OpenFaaS server to validate the credentials...
Cannot connect to OpenFaaS on URL: https://<public-ip>/openfaas. Get https://<public-ip>/openfaas/system/functions: x509: cannot validate certificate for <public-ip> because it doesn't contain any IP SANs
```

it seems openfaas requires TLS/SSL validation...

[ingress TLS](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)

[openfaas SSL](https://docs.openfaas.com/reference/ssl/kubernetes-with-cert-manager/)

remeber change letsencrypt-issuer staging server to `https://acme-staging-v02.api.letsencrypt.org/directory`

after setting TLS...

```bash
➜  cloud git:(master) ✗ faas-cli login --gateway https://xxx.compute-1.amazonaws.com/openfaas --password=f99883697dac5606416c112400b85351f82d2a1e
WARNING! Using --password is insecure, consider using: cat ~/faas_pass.txt | faas-cli login -u user --password-stdin
Calling the OpenFaaS server to validate the credentials...
Cannot connect to OpenFaaS on URL: https://xxx.compute-1.amazonaws.com/openfaas. Get https://xxx.compute-1.amazonaws.com/openfaas/system/functions: x509: certificate signed by unknown authority
```

change issuer from `staging` to `prod` in `tls.yml` abd `openfaas-crt.yaml`...

```bash
# crt NOT READY
➜  cloud git:(master) ✗ kubectl -n openfaas get certificate,secret openfaas-crtNAME                                          READY   SECRET         AGE
certificate.certmanager.k8s.io/openfaas-crt   False   openfaas-crt   4m

NAME                  TYPE                DATA   AGE
secret/openfaas-crt   kubernetes.io/tls   3      22m

➜  cloud git:(master) ✗ kubectl describe certificate openfaas-crt -n openfaas  
...
Status:
  Conditions:
    Last Transition Time:  2019-06-18T03:46:28Z
    Message:               Certificate issuance in progress. Temporary certificate issued.
    Reason:                TemporaryCertificate
    Status:                False
    Type:                  Ready
Events:
  Type    Reason        Age    From          Message
  ----    ------        ----   ----          -------
  Normal  OrderCreated  5m23s  cert-manager  Created Order resource "openfaas-crt-2327551295"
```

check the logs...

```bash
➜  cloud git:(master) ✗ kubectl logs svc/cert-manager-webhook -n cert-manager
```

[v0.7 on GKE stops after temporary cert (no order events or challenges)](https://github.com/jetstack/cert-manager/issues/1475)

change to version 0.8

```bash
➜  cloud git:(master) ✗ kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.8/deploy/manifests/00-crds.yaml

➜  cloud git:(master) ✗ kubectl create namespace cert-manager

➜  cloud git:(master) ✗ kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true

➜  cloud git:(master) ✗ helm install \
  --name cert-manager \
  --namespace cert-manager \
  --version v0.8.0 \
  jetstack/cert-manager

➜  cloud git:(master) ✗ kubectl apply -f openfaas/letsencrypt-issuer.yaml 

➜  cloud git:(master) ✗ helm upgrade openfaas \
    --namespace openfaas \
    --reuse-values \
    --values openfaas/tls.yml \
    openfaas/openfaas

➜  cloud git:(master) ✗ kubectl apply -f openfaas/openfaas-crt.yaml

# always stuck here even i re-create everything
I0618 04:45:45.643446       1 logger.go:38] Calling CreateOrder
E0618 04:45:45.726791       1 controller.go:200] cert-manager/controller/orders "msg"="re-queuing item  due to error processing" "error"="error creating new order: acme: urn:ietf:params:acme:error:rejectedIdentifier: Error creating new order :: Policy forbids issuing for name" "key"="openfaas/openfaas-crt-2327551295" 
I0618 04:45:55.727121       1 controller.go:198] cert-manager/controller/orders "level"=0 "msg"="syncing resource" "key"="openfaas/openfaas-crt-2327551295" 
I0618 04:45:55.727436       1 logger.go:38] Calling CreateOrder
E0618 04:45:55.827490       1 controller.go:200] cert-manager/controller/orders "msg"="re-queuing item  due to error processing" "error"="error creating new order: acme: urn:ietf:params:acme:error:rejectedIdentifier: Error creating new order :: Policy forbids issuing for name" "key"="openfaas/openfaas-crt-2327551295"
```

change namespace to `cert-manager-v08` and redo...

```bash
➜  cloud git:(master) ✗ kubectl describe certificate openfaas-crt -n openfaas
...
Status:
  Conditions:
    Last Transition Time:  2019-06-18T04:54:29Z
    Message:               Certificate issuance in progress. Temporary certificate issued.
    Reason:                TemporaryCertificate
    Status:                False
    Type:                  Ready
Events:
  Type    Reason              Age   From          Message
  ----    ------              ----  ----          -------
  Normal  Generated           18s   cert-manager  Generated new private key
  Normal  GenerateSelfSigned  18s   cert-manager  Generated temporary self signed certificate
  Normal  OrderCreated        18s   cert-manager  Created Order resource "openfaas-crt-2327551295"

# still get this error...
I0618 04:54:30.245632       1 controller.go:167] cert-manager/controller/certificates "level"=0 "msg"="syncing resource" "key"="openfaas/openfaas-crt" 
I0618 04:54:30.246345       1 issue.go:169] cert-manager/controller/certificates "level"=0 "msg"="Order is not in 'valid' state. Waiting for Order to transition before attempting to issue Certificate." "related_resource_kind"="Order" "related_resource_name"="openfaas-crt-2327551295" "related_resource_namespace"="openfaas" "resource_kind"="Certificate" "resource_name"="openfaas-crt" "resource_namespace"="openfaas"
I0618 04:54:30.247023       1 controller.go:173] cert-manager/controller/certificates "level"=0 "msg"="finished processing work item" "key"="openfaas/openfaas-crt"
...
I0618 04:57:06.047150       1 controller.go:198] cert-manager/controller/orders "level"=0 "msg"="syncing resource" "key"="openfaas/openfaas-crt-2327551295" 
I0618 04:57:06.047429       1 logger.go:38] Calling CreateOrder
E0618 04:57:07.172236       1 controller.go:200] cert-manager/controller/orders "msg"="re-queuing item  due to error processing" "error"="error creating new order: acme: urn:ietf:params:acme:error:rejectedIdentifier: Error creating new order :: Policy forbids issuing for name" "key"="openfaas/openfaas-crt-2327551295"
```

[Policy forbids issuing for name on Amazon EC2 domain](https://community.letsencrypt.org/t/policy-forbids-issuing-for-name-on-amazon-ec2-domain/12692)

WTF!
