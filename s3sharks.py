import boto3, os, json, threading, sys
from boto3.s3.transfer import TransferConfig
from s3hostweb import *
import pandas as pd
import re ## added 
import bs4
import sqlite3
import requests
import textwrap

'''
Let's pull some fresh shark data!

'''

res = requests.get('http://www.sharkresearchcommittee.com/pacific_coast_shark_news.htm')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

shark = []
for i in range(1, 100): # attempting to grab the most recent added paragraph 

    elems = soup.select('body > div > div > center > table > tr > td:nth-of-type(2) > p:nth-of-type({})'.format(i))
    for i in elems:
        #print("—" in str(i))
        if '—' in str(i):
            text = bs4.BeautifulSoup(str(i), 'html.parser')
            shark.append(text)
            #print(text)

'''

'''
c = sqlite3.connect('shark.db')
try:
    c.execute('''CREATE TABLE
                    mytable (Location        STRING,
                             Date            STRING,
                             Description     STRING)''')
except sqlite3.OperationalError: #i.e. table exists already
    pass

for n in shark:
        groups = re.match(r'(.*?)\W+—?\W+On\W+(.*?\d{4})\W*(.*)', str(n), flags=re.DOTALL)
        #print(n)
        if not groups:
            continue
        place, date, article = groups[1], groups[2], groups[3]
        
        
        c.execute('''INSERT INTO mytable(Location, Date, Description) VALUES(?,?,?)''',
            (place, date, article))
c.commit()
'''
Read into python [pandas] df
'''
df = pd.read_sql_query("select * from mytable;",c)
df.set_index('Location', inplace=True)



c.close()


'''
Store data into excel file that I will upload to S3 so others on team can acess
it
'''
writer = pd.ExcelWriter('sharksxlsx.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()
'''
Create bucket in S3, needs to be updated as of 7.9 not quite there
'''
BUCKET_NAME ='sharks-s3-2019-bucket'

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


def upload_small_file():
    file_path = os.path.dirname(__file__)+ '/sharksxlsx.xlsx'
    return s3_client().upload_file(file_path, BUCKET_NAME, 'sharksxlsx.xlsx')

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
    
    s3_client()
    s3_resource()
    create_bucket(BUCKET_NAME)
    upload_small_file()
    upload_large_file()
