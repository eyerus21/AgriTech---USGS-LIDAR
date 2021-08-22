import boto3
from botocore import UNSIGNED
from botocore.config import Config
import os

class Fetch:
    def __init__(self, bucket_name):
        self.s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        self.s3_resource = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
        self.bucket = self.s3_resource.Bucket(bucket_name)
 
    
    def fetch(self, remoteDirectoryName):
        # https://stackoverflow.com/questions/49772151/download-a-folder-from-s3-using-boto3
        for obj in self.bucket.objects.filter(Prefix = remoteDirectoryName):
            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            self.bucket.download_file(obj.key, obj.key)

if __name__ == "__ma  in__":
    fetch = Fetch(bucket_name="usgs-lidar-public")

    fetch.fetch("AK_BrooksCamp_2012")