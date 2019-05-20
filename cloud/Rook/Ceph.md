#

## ceph bluestore vs. filestore

> https://www.micron.com/about/blog/2018/may/ceph-bluestore-vs-filestoreblock-performance-comparison-when-leveraging-micron-nvme-ssds

## Ceph object gateway: s3-compatible

> http://docs.ceph.com/docs/master/radosgw/

![Ceph object gateway](http://docs.ceph.com/docs/master/_images/ditaa-50d12451eb76c5c72c4574b08f0320b39a42e5f1.png)

## adding/removing osds (expand/shrink cluster)

> http://docs.ceph.com/docs/mimic/rados/operations/add-or-rm-osds/

it's manual in ceph level but automatically in rook

## how to perform the access control for end user?

s3 has cloud front with [origin access identity](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html#private-content-granting-permissions-to-oai) and [signed urls & signed cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html)

ceph has this [MFA](http://docs.ceph.com/docs/mimic/radosgw/mfa/#re-sync-mfa-totp-token) but it is for removing objects...

then how to do access control?

a simple way is making all throughput passed through an api server, where this api server has access to s3 bucket, but this means the bandwidth of api server will be vastly occupied...

is it possible to generate a dynamic access token???
