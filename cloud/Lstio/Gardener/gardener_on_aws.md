#

## Gardener on AWS

[docs](https://gardener.cloud/using-gardener/developer/topic/)

[gardener_aws](https://gardener.cloud/050-tutorials/content/howto/gardener_aws/)

[installation](https://github.com/gardener/garden-setup)

[installer](https://gardener.cloud/installer/)

```bash
# create s3 bucket for state store
bucket_name=gardener-bucket

aws s3api create-bucket \
--bucket ${bucket_name} \
--region us-east-1

# env
export KOPS_CLUSTER_NAME=evaluate-gardener.k8s.local
export KOPS_STATE_STORE=s3://${bucket_name}

# create base cluster by kops
# garden requires at least 4 nodes with a size of 8GB for each node
kops create cluster \
--node-count=4 \
--node-size=t2.medium \
--master-size=t2.large \
--zones=us-east-1a \
--name=${KOPS_CLUSTER_NAME}
# create cluster
kops update cluster --name ${KOPS_CLUSTER_NAME} --yes
# validate cluster
kops validate cluster

# setup for calling sow via the wrapper
git clone "https://github.com/gardener/sow"
cd sow
export PATH=$PATH:$PWD/docker/bin
# create a directory landscape for your Gardener landscape and clone this repository into a subdirectory called crop
cd ..
mkdir landscape
cd landscape
git clone "https://github.com/gardener/garden-setup" crop
# export kubeconfig
kops export kubecfg --kubeconfig ./kubeconfig
# fill acre.yaml
sow convertkubeconfig
# display components installation order
sow order -A
# deploy Gardener
sow deploy -A
# find dashboard url
sow url
```

```bash
# by installer
# link: https://gardener.cloud/installer/
# fill in the form and get `gardener-deploy.yaml`
# deploy
kubectl apply -f gardener-deploy.yaml
# watch the installation process
kubectl logs -f garden-setup-installer
```

For error: `dial tcp: lookup xxx.xxx.xxx.xxx: no such host`
edit `/etc/resolv.conf`, set `nameserver 8.8.8.8`

[issue reference](https://github.com/gardener/gardener/issues/180)
