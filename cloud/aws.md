#

> https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html
>
> https://itnext.io/how-does-client-authentication-work-on-amazon-eks-c4f2b90d943b

## aws iam

* download aws-iam-authenticator
  * `curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/linux/amd64/aws-iam-authenticator`
  * `chmod +x ./aws-iam-authenticator`
  * `echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc`
  * `aws-iam-authenticator help`
* install aws cli
  * `pip3 install awscli --upgrade --user`
  * `aws --version`
* [config aws](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
  * `aws configure`
  * configure info should be got from aws iam console (My Credentials -> Access keys for CLI, SDK, & API access)
  * `aws eks list-clusters`
  * `aws s3 ls`

## create kubeconfig

> https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html

## create aws ec2 instances

take care of the **region**

`aws ec2 describe-availability-zones --region us-east-1`

## kops

> https://kubernetes.io/docs/setup/custom-cloud/kops/
>
> https://github.com/kubernetes/kops/blob/master/docs/aws.md
>
> https://medium.com/containermind/how-to-create-a-kubernetes-cluster-on-aws-in-few-minutes-89dda10354f4

* installation

```bash
wget https://github.com/kubernetes/kops/releases/download/1.10.0/kops-linux-amd64
chmod +x kops-linux-amd64
sudo mv kops-linux-amd64 /usr/local/bin/kops
```

* configure aws cli
  `aws config`

* create an aws s3 bucket for kops to persist its state

```bash
bucket_name=harold-kops-state
aws s3api create-bucket \
--bucket ${bucket_name} \
--region us-east-1

# enable versioning
aws s3api put-bucket-versioning --bucket ${bucket_name} --versioning-configuration Status=Enabled
```

* name k8s cluster and set s3 bucket URL in env var
    `export KOPS_CLUSTER_NAME=harold.k8s.local`
    `export KOPS_STATE_STORE=s3://${bucket_name}`

* create a Kubernetes cluster definition using kops by providing the required node count, node size, and AWS zones.

```bash
kops create cluster \
--node-count=2 \
--node-size=t2.micro \
--master-size=t2.micro \
--zones=us-east-1a \
--name=${KOPS_CLUSTER_NAME}
```

* review the k8s cluster definition
    `kops edit cluster --name ${KOPS_CLUSTER_NAME}`

* create k8s cluster on AWS
    `kops update cluster --name ${KOPS_CLUSTER_NAME} --yes`

* validate cluster
    `kops validate cluster`

* deploy k8s dashboard
    `kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml`

* find admin user's password
    `kops get secrets kube --type secret -oplaintext`

* find k8s master hostname
    `kubectl cluster-info`

* access the k8s dashboard using the following URL
    `https://<kubernetes-master-hostname>/ui`

* find the admin service account token
    `kops get secrets admin --type secret -oplaintext`

* delete the cluster
    `kops delete cluster --name ${KOPS_CLUSTER_NAME} --yes`