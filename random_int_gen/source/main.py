import random, json
from flask import jsonify

def execute(request):
    randomNum = random.randint(1,10)
    output = {"randomnum":randomNum}
    return jsonify(output)

   