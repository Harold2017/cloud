#

## kontena pharos

> https://www.kontena.io/pharos

## get started

> https://pharos.sh/docs/getting-started

* setup kontena pharos cli toolchain
  * install chpharos - the pharos version switcher tool
  `curl -s https://get.pharos.sh | bash`
  * login
  `chpharos login`
  * install phros cli tool binaries
  `chpharos install latest+oss --use`

* prepare nodes for k8s cluster
  * containers on linux distro

* create the cluster configuration file
  * yaml file

* bootstrap k8s cluster
  * in the same dir where cluster.yml file, run
  `pharos up -c cluster.yml` (--force if need update phraos)
  * watchout: if add nodes to the existed cluster, the new nodes should be in the same VPC (subnet) with cluster

* interact with the cluster
  * get kubeconfig file and run
  `pharos kubeconfig > kubeconfig`
  `export KUBECONFIG=./kubeconfig`