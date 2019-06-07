import googleapiclient.discovery
from flask import jsonify

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
    return jsonify(result)
