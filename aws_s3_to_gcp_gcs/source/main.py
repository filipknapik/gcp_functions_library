import boto3
import json
import os
from flask import jsonify
from google.cloud import storage

def execute(request):
    request_json = request.get_json()
    
    access_key_id = request_json['aws_access_key_id']
    secret_access_key = request_json['aws_secret_access_key']
    s3bucket = request_json['s3bucket']
    region_input = request_json['region_name']
    gcsbucket = request_json['gcsbucket']
    tempFileName = '/tmp/filedump'
    
    path = request_json['path']
    fileSize = readS3(access_key_id, secret_access_key, s3bucket, region_input, path, tempFileName) 
    if fileSize>0:
        return writeGCS(gcsbucket, path, tempFileName), 200
    return jsonfiy({"Result":"File not found or not downloaded from S3"}), 500
    

def readS3(access_key_id, secret_access_key, s3bucket, region_input, path, tempFileName):
    session = boto3.Session(aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
    s3 = session.resource('s3',region_name=region_input)

    s3.meta.client.download_file(s3bucket, path, tempFileName)
    
    fileSize = os.path.getsize(tempFileName)
    print("filesize="+str(os.path.getsize('/tmp/filedump')))
    return fileSize

def writeGCS(gcsbucket, path, tempFileName):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(gcsbucket)
    blob = bucket.blob(path)

    blob.upload_from_filename(tempFileName)
    return jsonify({"Result":"OK"})
