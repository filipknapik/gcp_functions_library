import requests
import json 

def execute(request):
    request_json = request.get_json()

    url_param = getParam('slackurl', request_json)
    message = getParam('message', request_json)

    body = {'text': message} 
    headers_struct = {'Content-type': 'application/json'}
   
    r = requests.post(url = url_param, data = json.dumps(body), headers = headers_struct) 
    return r.text

def getParam(param, request_json):
    if request_json and param in request_json:
        return request_json[param]
    else:
        return ''