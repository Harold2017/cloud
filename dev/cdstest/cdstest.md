#

## cds

> https://ovh.github.io/cds/hosting/ready-to-run/

## test cds with docker-compose (not use in production)

```bash
mkdir /tmp/cdstest && cd /tmp/cdstest
curl https://raw.githubusercontent.com/ovh/cds/master/docker-compose.yml -o docker-compose.yml
export HOSTNAME=$(hostname)

# Get the latest version
docker pull ovhcom/cds-ui:latest
docker pull ovhcom/cds-engine:latest

# Create PG database
docker-compose up --no-recreate -d cds-db

# check if DB is up
# check if last log is "LOG: database system is ready to accept connections"
docker-compose logs

docker-compose up --no-recreate cds-migrate
# You should have this log: "cds_cds-migrate_1 exited with code 0"

# run API and UI
docker-compose up -d cds-api cds-ui
```

### signup admin account

```bash
# register at http://localhost:2015/account/signup

# get URL for validate the registration and keep the password
docker-compose logs|grep 'verify/admin'
# WARNING: The HOSTNAME variable is not set. Defaulting to a blank string.
# click the URL
# obtain the info
{
  "user": {
    "id": 1,
    "username": "admin",
    "fullname": "admin",
    "email": "admin@local.local",
    "admin": true,
    "origin": "local",
    "favorites": null
  },
  "password": "474777a1db0361f9f139ed25ed33b3aef6d2c704acfacbd2cee3aa74b09fb0b666a313ddc4f9a05dbc64fd69066081fd85d871aa4560663f3db007b75696e0a7",
  "token": "6c52b33d-02a1-43cc-b044-55bec2f67a58"
}

```

### cdsctl

```bash
# download cdsctl CLI from http://localhost:2015/settings/downloads

# on a Linux workstation:
curl http://localhost:8081/download/cdsctl/linux/amd64 -o cdsctl

chmod +x cdsctl
./cdsctl login --api-url http://localhost:8081 -u admin -p 474777a1db0361f9f139ed25ed33b3aef6d2c704acfacbd2cee3aa74b09fb0b666a313ddc4f9a05dbc64fd69066081fd85d871aa4560663f3db007b75696e0a7
# cdsctl: You didn't specify config file location; /home/harold/.cdsrc will be used.

# test cdsctl
./cdsctl user me

# import a workflow template
./cdsctl template push https://raw.githubusercontent.com/ovh/cds/master/contrib/workflow-templates/demo-workflow-hello-world/demo-workflow-hello-world.yml
# Workflow template shared.infra/demo-workflow-hello-world has been created
# Template successfully pushed !

# create a project and create a workflow
./cdsctl project create DEMO FirstProject
./cdsctl workflow applyTemplate
```
