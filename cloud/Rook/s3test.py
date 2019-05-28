import boto.s3.connection
from boto.s3.key import Key
import json
import time


def create_conn():

    with open('credentials.json') as f:
        data = json.load(f)

    access_key = data["access_key"]
    secret_key = data["secret_key"]
    conn = boto.connect_s3(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            host=data["host"], port=data["port"],
            is_secure=False, calling_format=boto.s3.connection.OrdinaryCallingFormat(),
        )

    conn.auth_region_name = data["auth_region_name"]
    return conn

def test1():
    conn = create_conn()
    bucket = conn.create_bucket('my-new-bucket')
    for bucket in conn.get_all_buckets():
        print ("{name} {created}".format(
            name=bucket.name,
            created=bucket.creation_date,
        ))


def test2():
    conn = create_conn()
    b = conn.get_bucket('my-new-bucket')
    print(b.get_all_keys())
    bk = Key(b)
    bk.key = 'test'
    bk.set_contents_from_string('this is a test of s3 bucket object storage')
    print(bk.get_contents_as_string())


def test3():
    conn = create_conn()
    b = conn.get_bucket('my-new-bucket')
    fk = Key(b)
    fk.key = 'test_jpg'
    start = time.time()
    fk.set_contents_from_filename('test.jpg')
    print("time consumption: ", time.time() - start)
    start = time.time()
    fk.get_contents_to_filename('test_test.jpg')
    print("time consumption: ", time.time() - start)
    print(b.get_all_keys())

def test5():
    conn = create_conn()
    b = conn.get_bucket('my-new-bucket')
    fk = Key(b)
    fk.key = 'test_sb'
    start = time.time()
    fk.set_contents_from_filename('/home/harold/Desktop/dataset_expose/taiyou.sb')
    print("time consumption: ", time.time() - start)
    start = time.time()
    fk.get_contents_to_filename('test_sb.sb')
    print("time consumption: ", time.time() - start)
    print(b.get_all_keys())
    # time consumption:  102.47058463096619
    # time consumption:  885.4887373447418
    # [<Key: my-new-bucket,test>, <Key: my-new-bucket,test_jpg>, <Key: my-new-bucket,test_sb>]



if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    test5()
