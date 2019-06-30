import boto3
import json

BUCKET_NAME ='patrick-s3-2018-bucket'

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

def create_bucket_policy():
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement":[
            {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action":["s3:*"],
            "Resource":["arn:aws:s3:::patricksbucket/*"]
            }
        ]
    }
    policy_string = json.dumps(bucket_policy)
    
    return s3_client().put_bucket_policy(
        Bucket=BUCKET_NAME,
        Policy=policy_string
    )
if __name__ == '__main__':
    print(create_bucket(BUCKET_NAME))
    #print(create_bucket_policy())
