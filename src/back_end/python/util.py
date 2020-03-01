import json, requests, configparser,uuid
from urllib.parse import urlencode
from urllib.request import urlretrieve
from google.cloud import storage
import os, datetime
import smtplib, ssl
from email.mime.text import MIMEText

def send_notification_slack(WEB_HOOK_URL, send_message):
    requst_data = json.dumps({'text': send_message})
    requests.post(WEB_HOOK_URL, requst_data)

def config_pase(cfg_name):
    cfg_path = "../../../property/back_end/python/config.ini"
    cfg = configparser.ConfigParser()
    cfg.read(cfg_path)
    cfg_value = cfg["default"][cfg_name]
    return cfg_value

def create_tmp_file(random_num, username, email):
    content = [username, email]
    out_contents = ','.join(content)
    file_path = config_pase("tmp_file_path")
    file_name = file_path + random_num + '.txt'
    fout = open(file_name, 'wt')
    print(out_contents, file=fout, end='\n')
    fout.close()
    return None

def generate_random_num():
    return str(uuid.uuid4())

def generate_return_url(uuid, destination):
    d_destination = destination
    get_pram_dict = {'uuid': uuid}
    query_string = urlencode(get_pram_dict)
    return_url = d_destination + query_string

    yes_url = return_url + '&res=1'
    no_url = return_url + '&res=0'

    return yes_url, no_url

def send_notification_mail():

    link_url = generate_download_signed_url_v4('static-ctn-app', 'portfolio.html')

    gmail_account = config_pase("gmail_account")
    gmail_password = config_pase("gmail_password")

    mail_to = config_pase("mail_to")

    subject = "Result of your requested for contents view"
    body = f'You can access contents using below URL\n {link_url}'

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,timeout=10)
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")


def generate_download_signed_url_v4(bucket_name, object_name):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config_pase("google_application_credentials_path")
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)

    url = blob.generate_signed_url(
        version='v4',
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method='GET')

    print('Generated GET signed URL:')
    return url