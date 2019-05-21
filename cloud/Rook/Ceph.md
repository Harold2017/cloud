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

## access control

### S3

> https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-access-control.html
> https://aws.amazon.com/blogs/security/iam-policies-and-bucket-policies-and-acls-oh-my-controlling-access-to-s3-resources/
- ID / emailAdress (aws)
- AllUsers (Anyone can PUT or GET)
- ACL/ACP (Lists and Policies, can be set on the bucket or objects inside)
  - [Using Bucket Policies and User Policies](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html)
    - user policies (IAM policies): whole IAM env, more than just buckets
    - s3 bucket policies: whole s3 env, know who can access a bucket
  - [Managing Access with ACLs](https://docs.aws.amazon.com/AmazonS3/latest/dev/S3_ACLs_UsingACLs.html)
    - buckets and objects
  - [Using Amazon S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html)
    - a certain bucket
    - 2 levels: account/bucket
    - > Amazon S3 doesn't support block public access settings on a per-object basis.
    - > When you apply block public access settings to an account, the settings apply to all AWS Regions globally. The settings might not take effect in all Regions immediately or simultaneously, but they eventually propagate to all Regions.

![Block public access (account settings)](https://docs.aws.amazon.com/AmazonS3/latest/dev/images/block-public-access-account-settings.png)

**Permissions**

| Operation                                   | Required Permissions           |
|---------------------------------------------|--------------------------------|
| GET bucket policy status                    | s3:GetBucketPolicyStatus       |
| GET bucket Block Public Access settings     | s3:GetBucketPublicAccessBlock  |
| PUT bucket Block Public Access settings     | s3:PutBucketPublicAccessBlock  |
| DELETE bucket Block Public Access settings  | s3:PutBucketPublicAccessBlock  |
| GET account Block Public Access settings    | s3:GetAccountPublicAccessBlock |
| PUT account Block Public Access settings    | s3:PutAccountPublicAccessBlock |
| DELETE account Block Public Access settings | s3:PutAccountPublicAccessBlock |

3 ways applying Block Public Access:

- AWS CLI
- AWS SDK
- REST APIs (Authorization header)
  - Account-level operations
    - [PUT PublicAccessBlock](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTAccountPUTPublicAccessBlock.html)
    - [GET PublicAccessBlock](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTAccountGETPublicAccessBlock.html)
    - [DELETE PublicAccessBlock](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTAccountDELETEPublicAccessBlock.html)
  - Bucket-level operations
    - [PUT PublicAccessBlock](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTPublicAccessBlock.html)
    - [GET PublicAccessBlock](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETPublicAccessBlock.html)
    - [DELETE PublicAccessBlock](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketDELETEPublicAccessBlock.html)
    - [GET BucketPolicyStatus](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETPolicyStatus.html)

Sample:

```bash
PUT /v20180820/configuration/publicAccessBlock HTTP/1.1
Host: <account-id>.s3-control.amazonaws.com
x-amz-date: <Thu, 15 Nov 2016 00:17:21 GMT>
Authorization: <signatureValue>

<?xml version="1.0" encoding="UTF-8"?>
<PublicAccessBlockConfiguration>
      <BlockPublicAcls>TRUE</BlockPublicAcls> 
      <IgnorePublicAcls>FALSE</IgnorePublicAcls> 
      <BlockPublicPolicy>FALSE</BlockPublicPolicy> 
      <RestrictPublicBuckets>FALSE</RestrictPublicBuckets>
</PublicAccessBlockConfiguration>
```

HMAC:

![AWS Signature Version 4](https://docs.aws.amazon.com/AmazonS3/latest/API/images/signing-overview.png)

AWS CloudFont:

[Serving Private Content with Signed URLs and Signed Cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html)

> You can control user access to your private content in two ways, as shown in the following illustration:
>
> - Restrict access to files in CloudFront edge caches
> - Restrict access to files in your Amazon S3 bucket (unless you've configured it as a website endpoint)

![AWS CloudFont](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/images/PrivateContent_TwoParts.png)

**Restricting Access to Files in CloudFront Edge Caches:**

> When you create signed URLs or signed cookies to control access to your files, you can specify the following restrictions:
>
> - An ending date and time, after which the URL is no longer valid.
> - (Optional) The date and time that the URL becomes valid.
> - (Optional) The IP address or range of addresses of the computers that can be used to access your content.

**Restricting Access to Files in Amazon S3 Buckets:**

> To require that users access your content through CloudFront URLs, you perform the following tasks:
>
> - Create a special CloudFront user called an origin access identity.
> - Give the origin access identity permission to read the files in your bucket.
> - Remove permission for anyone else to use Amazon S3 URLs to read the files.

**Using an HTTP Server for Private Content:**

> You can use signed URLs or signed cookies for any CloudFront distribution, regardless of whether the origin is an Amazon S3 bucket or an HTTP server. However, for CloudFront to get your files from an HTTP server, the files must remain publicly accessible. When the files are publicly accessible, anyone who has the URL for a file on your HTTP server can access the file without logging in or paying for your content. If you use signed URLs or signed cookies and your origin is an HTTP server, do not give the URLs for the files on your HTTP server to your customers or to others outside your organization.

### ceph

> http://docs.ceph.com/docs/firefly/rados/operations/auth-intro/
> All Ceph object store clients use the **librados** library to interact with the Ceph object store.

![C/S stack](http://docs.ceph.com/docs/firefly/_images/ditaa-d4b739f8889e03e5d72abddb26ce74425e540539.png)

> To use cephx, an administrator must set up users first.
> ![create user](http://docs.ceph.com/docs/firefly/_images/ditaa-6b1dafb6d8f177ab2beb3325857f1e98e4593ec6.png)
> ![session](http://docs.ceph.com/docs/firefly/_images/ditaa-56e3a72e085f9070289331d64453b84ab1e9510b.png)

**Limitations:**

> In particular, arbitrary user machines, especially portable machines, should not be configured to interact directly with Ceph, since that mode of use would require the storage of a plaintext authentication key on an insecure machine. Anyone who stole that machine or obtained surreptitious access to it could obtain the key that will allow them to authenticate their own machines to Ceph.
>
> Rather than permitting potentially insecure machines to access a Ceph object store directly, users should be required to sign in to a trusted machine in your environment using a method that provides sufficient security for your purposes. That trusted machine will store the plaintext Ceph keys for the human users. A future version of Ceph may address these particular authentication issues more fully.
>
> At the moment, none of the Ceph authentication protocols provide secrecy for messages in transit. Thus, an eavesdropper on the wire can hear and understand all data sent between clients and servers in Ceph, even if he cannot create or alter them. Further, Ceph does not include options to encrypt user data in the object store. Users can hand-encrypt and store their own data in the Ceph object store, of course, but Ceph provides no features to perform object encryption itself. Those storing sensitive data in Ceph should consider encrypting their data before providing it to the Ceph system.