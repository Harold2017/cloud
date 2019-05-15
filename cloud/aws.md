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

## aws new cluster

> https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
> https://docs.aws.amazon.com/vpc/latest/userguide/getting-started-ipv4.html

- create new vpc
- create new subnet
- create new route table
- create new internet gateway and attach it to vpc
- route table edit routes and add new route, target choose `Internet Gateway`, choose former gateway, add destination (0.0.0.0/0 for all traffic)

## pharos create kubeconfig from cluster.yml

- theoretically you should config only one instance has internet connection and use it as host for Pharos to config all others through private ips
- but since i use my local PC as host, so every instances should has internet connection to let Pharos ssh into it

## next part divided into two tools: kops and Pharos

find details in corresponding .md file
