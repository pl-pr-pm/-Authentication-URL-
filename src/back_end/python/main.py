from flask import Flask, request
import json, requests, configparser

app = Flask(__name__)

@app.route('/request-authentification-url' , methods=['POST'])
def send_notification():

    username = request.form.get('username')
    email = request.form.get('email')

    WEB_HOOK_URL = config_pase("webhook_path")

    send_message = f'You requested for Authentification url of GCS from \n<{username}>\n<{email}>.\n Do you know anything about it?'

    requst_data = json.dumps({'text': send_message})

    requests.post(WEB_HOOK_URL, requst_data)

    return "response is done. Please wait finish of check your request."


def config_pase(cfg_name):
    cfg_path = "/Users/Ryo_Ito/work/project/create_authentification_url_for_GCS_uploaded/property/back_end/python/config.ini"
    cfg = configparser.ConfigParser()
    cfg.read(cfg_path)
    cfg_value = cfg["default"][cfg_name]
    print(cfg_value)
    return cfg_value
