import os
from google.cloud import kms_v1
from google.cloud import firestore
from flask import jsonify

def execute(request):
    request_json = request.get_json()

    if request_json:
        if 'action' in request_json:
            action = request_json['action']
            
            GCP_PROJECT = os.environ.get('GCP_PROJECT', '')
            KEY_RING = os.environ.get('KEY_RING', '')
            CRYPTO_KEY = os.environ.get('CRYPTO_KEY', '')
            LOCATION = os.environ.get('LOCATION','global')
            
            if action == 'storesecret':
                key = request_json['key']
                secret = request_json['secret']
                return saveSecret(GCP_PROJECT, LOCATION, KEY_RING, CRYPTO_KEY, key, secret)       
            elif action == 'getsecrets':
                return getSecrets(GCP_PROJECT, LOCATION, KEY_RING, CRYPTO_KEY)
    return "action not understood"

def encrypt(project_id, location_id, key_ring_id, crypto_key_id,inputstr):
    
    client = kms_v1.KeyManagementServiceClient()
    plaintext = inputstr.encode('UTF-8')
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,crypto_key_id)

    response = client.encrypt(name, plaintext)
    return response.ciphertext

def decrypt(project_id, location_id, key_ring_id, crypto_key_id,inputbytes):
    
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,crypto_key_id)

    response = client.decrypt(name, inputbytes)
    return response.plaintext

def saveKey(key, value):
    print("key:"+str(key))
    print("value:"+str(value))
    db = firestore.Client()
    # [START quickstart_add_data_one]
    doc_ref = db.collection('secrets').document(key)
    doc_ref.set({
        'encrypted': value
    })
    return "OK"

def saveSecret(GCP_PROJECT, LOCATION, KEY_RING, CRYPTO_KEY, key, secret):
    secret_encrypted = encrypt(GCP_PROJECT, LOCATION, KEY_RING, CRYPTO_KEY, secret)
    saveKey(key,secret_encrypted)
    return "OK"
    
def getSecrets(GCP_PROJECT, LOCATION, KEY_RING, CRYPTO_KEY):
    db = firestore.Client()
    secrets_ref = db.collection('secrets')
    docs = secrets_ref.get()
    output = {}

    for doc in docs:
        key = doc.id
        encryptedDict = doc.to_dict()
        encryptedSecret = encryptedDict['encrypted']
        decryptedSecret = decrypt(GCP_PROJECT, LOCATION, KEY_RING, CRYPTO_KEY,encryptedSecret)
        output[key] = decryptedSecret.decode("utf-8") 
    return jsonify(output)