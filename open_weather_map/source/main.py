import requests
import json 
from flask import jsonify

def execute(request):
    request_json = request.get_json()

    url = 'http://api.openweathermap.org/data/2.5/weather'
    location = getParam('city', request_json)
    appid = getParam('appid', request_json)
    payload = {'q': location, 'APPID':appid}
    r = requests.get(url, params=payload)
    
    return jsonify(r.text)

def getParam(param, request_json):
    if request_json and param in request_json:
        return request_json[param]
    else:
        return ''