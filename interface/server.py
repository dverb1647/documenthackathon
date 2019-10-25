#!/usr/bin/env python3

from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import boto3
import subprocess
import requests

import analyzeShapes

app = Flask(__name__)
VAULT_ADDR = 'https://vault.eng.appianci.net'
AWS_SESSION_CREDENTIALS = {
    'last_updated': datetime.now() - timedelta(hours=24),
    'aws_access_key_id': None,
    'aws_secret_access_key': None,
    'aws_session_token': None
}

def refresh_aws_session_credentials():
    global AWS_SESSION_CREDENTIALS

    # Get a token for an application role via get-vault-token
    environ['VAULT_KUBERNETES_AUTH_BACKEND_ROLE'] = 'rekognition-detect-text-principal-role'
    completed_process = subprocess.run(['get-vault-token', '--application', 'rekognition-detect-text'], stdout=subprocess.PIPE, check=True)
    application_token = completed_process.stdout.decode().strip()

    # Use the token to read a secret from Vault via Vault's REST API. Access the
    # JSON from the response as a Python object
    url = f'{VAULT_ADDR}/v1/prod.aws/creds/rekognition-detect-text'
    response = requests.get(url, headers={'X-Vault-Token': application_token})
    response.raise_for_status()
    r = response.json()

    AWS_SESSION_CREDENTIALS = {
        'last_updated': datetime.now(),
        'aws_access_key_id': r['data']['access_key'],
        'aws_secret_access_key': r['data']['secret_key'],
        'aws_session_token': r['data']['security_token']
    }


@app.route('/api/interface/dummy')
def dummy():
    return jsonify({
        "success": True,
        "data": {}
    })

@app.route('/api/interface/generate', methods=['POST'])
def interface_generate():
    global AWS_SESSION_CREDENTIALS

    if datetime.now() - AWS_SESSION_CREDENTIALS['last_updated'] > timedelta(minutes=55):
        refresh_aws_session_credentials()

    image = request.files['image']
    client = boto3.client(
        'rekognition',
        region_name='us-east-1',
        aws_access_key_id=AWS_SESSION_CREDENTIALS['aws_access_key_id'],
        aws_secret_access_key=AWS_SESSION_CREDENTIALS['aws_secret_access_key'],
        aws_session_token=AWS_SESSION_CREDENTIALS['aws_session_token'])

    # TODO

    data = analyzeShapes.main(request.files['image'])

    return jsonify({
        "success": True,
        "data": data
    })

if __name__ == '__main__':
    app.run(debug=True)
