import random, json
from flask import jsonify

def execute(request):
    randomNum = random.randint(1,10)
    output = {"slackresponse":randomNum}
    return jsonify(output)

   