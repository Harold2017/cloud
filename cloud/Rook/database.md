#

## mysql on rook/ceph

- use `mysql.yaml` to launch a mysql pod
- `running` at beginning, but after several seconds, the status becomes `Unknown`, and one node `lost` (`agent`, `mon`, `osd`, `discover` on that node becomes `NodeLost`, rbd on that node becomes `Unknown`)

    ```bash
    ➜  Rook git:(master) ✗ kubectl get nodes
    NAME                            STATUS     ROLES    AGE    VERSION
    ip-172-20-35-247.ec2.internal   Ready      node     5d5h   v1.12.7
    ip-172-20-55-182.ec2.internal   NotReady   node     5d5h   v1.12.7
    ip-172-20-57-215.ec2.internal   Ready      master   5d5h   v1.12.7
    ip-172-20-63-39.ec2.internal    Ready      node     5d5h   v1.12.7
    ```

- > https://github.com/kubernetes/kubernetes/issues/46349
- try `reboot` the node does NOT work, have to `terminate` it and KOPS recreate one automatically
- this time it works well and the mysql pod started but one `osd` is in `pending` status
- enter in `mysql` pod, and try to create one db, it stuck here and `NodeLost` again

    ```bash
    ➜  Rook git:(master) ✗ kubectl get pods
    NAME                                      READY   STATUS     RESTARTS   AGE
    mysql-5bc4f5b94b-dgshb                    1/1     Running    0          10m
    rook-ceph-agent-9gp7l                     1/1     NodeLost   0          2d6h
    rook-ceph-agent-sdxnc                     1/1     Running    0          2d6h
    rook-ceph-agent-wpksh                     1/1     Running    0          14m
    rook-ceph-mgr-a-7954598d69-f95xf          1/1     Unknown    0          2d6h
    rook-ceph-mgr-a-7954598d69-hth2j          1/1     Running    0          2m50s
    rook-ceph-mon-a-79dc4fd9d4-dkxng          1/1     Running    0          2d6h
    rook-ceph-mon-c-dbb9d7f5d-742sl           1/1     Unknown    0          2d6h
    rook-ceph-mon-c-dbb9d7f5d-xvbdf           0/1     Pending    0          2m50s
    rook-ceph-mon-d-66667fbb87-kk9m6          1/1     Running    0          13m
    rook-ceph-operator-5d495fcb75-2xxnl       1/1     Running    0          2m50s
    rook-ceph-operator-5d495fcb75-grxwd       1/1     Unknown    1          2d6h
    rook-ceph-osd-0-7557dd7cf5-k2n67          1/1     Running    0          2d6h
    rook-ceph-osd-1-58456c9875-6qwd6          0/1     Pending    0          2m50s
    rook-ceph-osd-1-58456c9875-8gqsq          1/1     Unknown    0          2d6h
    rook-ceph-osd-2-6b66bdcd89-bc2hq          0/1     Pending    0          6m22s
    rook-ceph-rgw-my-store-5ddc4784cc-wntb2   1/1     Running    0          2d3h
    rook-ceph-tools-689646bb64-pjr2t          1/1     Running    0          2d6h
    rook-discover-9cjn9                       1/1     Running    0          2d6h
    rook-discover-qr9km                       1/1     Running    0          14m
    rook-discover-v992w                       1/1     NodeLost   0          2d6h
    test-pod3-rbd                             1/1     Unknown    0          6h12m
    ```

- stop creating, got following error:

    ```bash
    ^CCtrl-C -- sending "KILL QUERY 2" to server ...
    Ctrl-C -- query aborted.
    ^CCtrl-C -- sending "KILL 2" to server ...
    Ctrl-C -- query aborted.
    ERROR 2013 (HY000): Lost connection to MySQL server during query
    mysql> show databases;
    ERROR 2006 (HY000): MySQL server has gone away
    No connection. Trying to reconnect...
    Connection id:    5
    Current database: *** NONE ***

    ^CCtrl-C -- sending "KILL QUERY 5" to server ...
    Ctrl-C -- query aborted.
    ^CCtrl-C -- sending "KILL 5" to server ...
    Ctrl-C -- query aborted.
    ERROR 2013 (HY000): Lost connection to MySQL server during query
    mysql> Ctrl-C -- exit!
    Aborted
    ```

- enter `mysql` pod again, former `test_db` created?

    ```bash
    mysql> show databases;
    +---------------------+
    | Database            |
    +---------------------+
    | information_schema  |
    | #mysql50#lost+found |
    | mysql               |
    | performance_schema  |
    | test                |
    | test_db             |
    +---------------------+
    6 rows in set (0.00 sec)

    mysql> show tables;
    +-------------------+
    | Tables_in_test_db |
    +-------------------+
    | test              |
    +-------------------+
    1 row in set (0.03 sec)

    mysql> insert into test
        -> (title)
        -> values
        -> ("test")
        -> ;
    Query OK, 1 row affected (0.08 sec)

    mysql> select * from test;
    +---------+-------+
    | test_id | title |
    +---------+-------+
    |       1 | test  |
    +---------+-------+
    1 row in set (0.06 sec)
    ```

- `mysql` works well... strange... why `NodeLost`?
- `rook` recovered by itself...

    ```bash
    ➜  Rook git:(master) ✗ kubectl get pods
    NAME                                                        READY   STATUS      RESTARTS   AGE
    mysql-5bc4f5b94b-dgshb                                      1/1     Running     0          24m
    rook-ceph-agent-9gp7l                                       1/1     Running     1          2d6h
    rook-ceph-agent-sdxnc                                       1/1     Running     0          2d6h
    rook-ceph-agent-wpksh                                       1/1     Running     0          28m
    rook-ceph-mgr-a-7954598d69-hth2j                            1/1     Running     0          16m
    rook-ceph-mon-a-79dc4fd9d4-dkxng                            1/1     Running     0          2d6h
    rook-ceph-mon-c-dbb9d7f5d-xvbdf                             1/1     Running     0          16m
    rook-ceph-mon-d-66667fbb87-kk9m6                            1/1     Running     0          27m
    rook-ceph-operator-5d495fcb75-2xxnl                         1/1     Running     0          16m
    rook-ceph-osd-0-7557dd7cf5-k2n67                            1/1     Running     0          2d6h
    rook-ceph-osd-1-58456c9875-6qwd6                            1/1     Running     0          16m
    rook-ceph-osd-2-6b66bdcd89-bc2hq                            0/1     Pending     0          20m
    rook-ceph-osd-3-7b6557b7cb-dmwl5                            1/1     Running     0          8m19s
    rook-ceph-osd-prepare-ip-172-20-35-247.ec2.internal-q5gx4   0/2     Completed   1          8m29s
    rook-ceph-osd-prepare-ip-172-20-38-207.ec2.internal-mpm6n   0/2     Completed   0          8m29s
    rook-ceph-osd-prepare-ip-172-20-63-39.ec2.internal-khm4w    0/2     Completed   0          8m27s
    rook-ceph-rgw-my-store-5ddc4784cc-ldgv2                     1/1     Running     0          7m45s
    rook-ceph-tools-689646bb64-pjr2t                            1/1     Running     0          2d6h
    rook-discover-9cjn9                                         1/1     Running     0          2d6h
    rook-discover-qr9km                                         1/1     Running     0          28m
    rook-discover-v992w                                         1/1     Running     1          2d6h
    ```

- may be related to this? [kubernetes-nodelost-notready-high-io-disks](https://stackoverflow.com/questions/50479212/kubernetes-nodelost-notready-high-io-disks)

## redis on rook/ceph

it is very complicated to start a redis cluster with single yaml file...

try to use helm

> https://github.com/helm/charts/tree/master/stable/redis-ha

## mongodb / mysql with helm

> https://github.com/helm/charts/tree/master/stable/mongodb
> https://github.com/helm/charts/tree/master/stable/mysql

helm is awesome!
