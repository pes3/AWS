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
def list_buckets():
    return s3_client().list_buckets()

##def get_bucket_policy():
##    return s3_client().get_bucket_policy(Bucket='patrick-s3-2018-bucket')

def get_bucket_encryption():

    return s3_client().get_bucket_encryption(Bucket=BUCKET_NAME)

#aware server side encryption was not found

##script not done below, as of 6.29.19

def update_bucket_policy(bucket_name):
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                "Sid": "AddPerm",
                "Effect": "Allow",
                "Principal": "*",
                "Action":[
                    's3:DeleteObject',
                    's3:GetObject',
                    's3:PutObject'
                ],
                'Resource':'arn:aws:s3:::' + bucket_name + '/*'
            }
        ]
    }
    policy_string = json.dumps(bucket_policy)

    return s3_client().put_bucket_policy(
        Bucket=BUCKET_NAME,
        Poicy=policy_string
        )
if __name__ == '__main__':
    update_bucket_policy(BUCKET_NAME)