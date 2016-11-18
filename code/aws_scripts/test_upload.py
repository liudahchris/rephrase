import pandas as pd
import numpy as np
import boto
import os

def get_aws_access():
    return os.environ['AWS_ACCESS_KEY'], os.environ['AWS_SECRET_ACCESS_KEY']

def s3_upload_string(bucket_name,data,fname):
    access_key, secret_access_key = get_aws_access()
    conn = boto.connect_s3(access_key, secret_access_key)
    if conn.lookup(bucket_name) is None:
        bucket = conn.create_bucket(bucket_name, policy='public-read')
    else:
        bucket = conn.get_bucket(bucket_name)
    key = bucket.new_key(fname)
    key.set_contents_from_string(data)

def s3_upload_filename(bucket_name,path,fname):
    access_key, secret_access_key = get_aws_access()
    conn = boto.connect_s3(access_key, secret_access_key)
    if conn.lookup(bucket_name) is None:
        bucket = conn.create_bucket(bucket_name, policy='public-read')
    else:
        bucket = conn.get_bucket(bucket_name)
    key = bucket.new_key(fname)
    key.set_contents_from_filename(path)

if __name__=='__main__':
    # BUCKETNAME = 'liudahchris-test-bucket'
    # FNAME = 'test_file.csv'
    # df = pd.DataFrame(data=np.array([range(0,5),range(5,10)]))
    # s3_upload_string(BUCKETNAME,df.to_csv(),FNAME)


    BUCKETNAME = 'liudahchris'
    fname = 'track_metadata.db'
    path = '/mnt/snap/AdditionalFiles/{}'.format(fname)
    s3_upload_filename(BUCKETNAME,path,fname)
