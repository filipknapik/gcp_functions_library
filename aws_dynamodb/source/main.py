import boto3
import json
from flask import jsonify

def execute(request):
    request_json = request.get_json()
    
    access_key_id = request_json['aws_access_key_id']
    secret_access_key = request_json['aws_secret_access_key']
    table_name = request_json['table_name']
    region_input = request_json['region_name']
    
    if request_json['action']=='read':
        key = request_json['key']
        return readDynamoDB(access_key_id, secret_access_key, table_name, region_input, key) 
    elif request_json['action']=='write':
        item = request_json['item']
        return writeDynamoDB(access_key_id, secret_access_key, table_name, region_input, item) 
    return "method not found"


def readDynamoDB(access_key_id, secret_access_key, table_name, region_input, key):
    session = boto3.Session(aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
    dynamodb = session.resource('dynamodb',region_name=region_input)
    table = dynamodb.Table(table_name)

    response = table.get_item(Key=key)
    return jsonify(response["Item"])

def writeDynamoDB(access_key_id, secret_access_key, table_name, region_input, key, value):
    # needs to be completed & tested still!
    session = boto3.Session(aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
    dynamodb = session.resource('dynamodb',region_name=region_input)
    table = dynamodb.Table(table_name)
    
    response = table.update_item(
        Key=key,
        AttributeUpdates=value
    )
    return jsonify({"Result":"OK"})