from flask import Flask, request
from pathlib import Path
from util import create_tmp_file, config_pase, send_notification_slack, generate_random_num, generate_return_url,generate_download_signed_url_v4,send_notification_mail

app = Flask(__name__)

@app.route('/request-authentification-url' , methods=['POST'])
def send_notification():

    username = request.form.get('username')
    email = request.form.get('email')
    uuid = generate_random_num()

    try:
        create_tmp_file(uuid,username, email)
    except Exception:
        return "Something happens. Please retry request."

    WEB_HOOK_URL = config_pase("webhook_path")
    answer_url = config_pase('answer_url') + '?'

    yes_url, no_url = generate_return_url(uuid, answer_url)

    send_message = f'You requested for Authentification url of GCS from \n<{username}>\n<{email}>\n Do you know anything about it?\n <{yes_url}|*YES*> <{no_url}|*NO*>'
    send_notification_slack(WEB_HOOK_URL, send_message)

    return "Please wait finish of check your request."

@app.route('/generate-authentification-url' , methods=['GET'])
def generate_authentification_url():
    send_notification_mail()
    return "Please wait finish of check your request."

if __name__ == "__main__":
    app.run(debug=True)