#!/usr/bin/env python3

from flask import Flask, jsonify, request
from os import environ
from datetime import datetime, timedelta
import subprocess
import requests


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

@app.route('/api/interface/generate')
def interface_generate():
    global AWS_SESSION_CREDENTIALS

    if datetime.now() - AWS_SESSION_CREDENTIALS['last_updated'] > timedelta(minutes=55):
        refresh_aws_session_credentials()



    # data = '''
    # {
    #     a!textField(
    #         label: "Label"
    #     )
    # }
    # '''

    return jsonify({
        "success": True,
        "data": AWS_SESSION_CREDENTIALS
    })

if __name__ == '__main__':
    app.run(debug=True)
