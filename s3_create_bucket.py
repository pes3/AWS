import boto3
import json

BUCKET_NAME ='patrick-s3-2019-bucket'

def s3_client():
    s3 = boto3.client('s3')
    """:type : pyboto3.s3"""
    return s3

def create_bucket(bucket_name):
    return s3_client().create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-2'
            }
        )

if __name__ == '__main__':
    print(create_bucket(BUCKET_NAME))
    #print(create_bucket_policy())
