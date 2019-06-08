import googleapiclient.discovery
from flask import jsonify
import os

def execute(request):
    compute = googleapiclient.discovery.build('compute', 'v1')
    request_json = request.get_json()
    
    instanceid = request_json['instance']
    action = request_json['action']
    zoneid = request_json['zone']
    
    GCP_PROJECT = os.environ.get('GCP_PROJECT', '')
    
    if action=='stop':
        result = compute.instances().stop(project=GCP_PROJECT, zone=zoneid, instance=instanceid).execute()
    elif action=='start':
        result = compute.instances().start(project=GCP_PROJECT, zone=zoneid, instance=instanceid).execute()
    elif action=='getdetails':
        result = compute.instances().list(project=GCP_PROJECT, zone=zoneid).execute()
        items = result["items"]
        result = {"Error":"instance not found"}
        for item in items:
            if item["name"]==instanceid:
                result = item
    return jsonify(result), 200
