import boto3
import json
import os
import threading
import sys
from boto3.s3.transfer import TransferConfig

BUCKET_NAME ='patrick-s3-2019-bucket'

def s3_client():
    s3 = boto3.client('s3')
    """:type : pyboto3.s3"""
    return s3
def s3_resource():
    s3 = boto3.resource('s3')
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
            "Resource":["arn:aws:s3:::patrick-s3-2019-bucket/*"]
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

def get_bucket_policy():
    return s3_client().get_bucket_policy(Bucket='patrick-s3-2018-bucket')

def get_bucket_encryption():

    return s3_client().get_bucket_encryption(Bucket=BUCKET_NAME)



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
        Policy=policy_string
        )

def server_side_encrypt_bucket():
    return s3_client().put_bucket_encryption(
        Bucket=BUCKET_NAME,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault':{
                        'SSEAlgorithm':'AES256'
                        }
                    }
                ]
            }
        )


def delete_bucket():
    return s3_client().delete_bucket(Bucket=BUCKET_NAME)


def upload_small_file():
    file_path = os.path.dirname(__file__)+ '/test.txt'
    return s3_client().upload_file(file_path, BUCKET_NAME, 'test.txt')

def upload_large_file():
    config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
                            multipart_chunksize=1024 * 25, use_threads=True)
    file_path = os.path.dirname(__file__) + '/largefile.pdf'
    key_path = 'multipart_files/largefile.pdf'
    s3_resource().meta.client.upload_file(file_path, BUCKET_NAME, key_path, ExtraArgs = {'ACL': 'public-read',
                                                                                        'ContentType': 'text/pdf'},
                                          Config =config,
                                          Callback=ProgressPercentage(file_path))
class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename=filename
        self.size= float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock= threading.Lock()
    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far+= bytes_amount
            percentage = (self._seen_so_far / self.size) * 100
            sys.stdout.write(
                "\r%s  %s / %s (%.2f%%)" % (
                    self._filename, self._seen_so_far, self.size,
                    percentage
                    )
                )
            sys.stdout.flush()
            
            

    
                                                                              
    
    

if __name__ == '__main__':
    #print(create_bucket(BUCKET_NAME))
    #update_bucket_policy(BUCKET_NAME)
    #print(server_side_encrypt_bucket())
    #print(delete_bucket())
    print(upload_large_file())
