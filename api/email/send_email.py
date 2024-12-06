import os
import smtplib
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


email_bp = Blueprint('email_bp', __name__)

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("APP_MAIL_PASS")
RECAPTCHA_SECRET_KEY = os.getenv("CAPTCHA_SECRET_KEY")

'''
def get_app_password():
    email_password = os.getenv('APP_MAIL_PASS')
    return email_password
def get_app_password_temp() :
    return os.environ['APP_MAIL_PASS']

GMAIL_APP_PASSWORD = get_app_password() 
RECAPTCHA_SECRET_KEY = os.getenv("CAPTCHA_SECRET_KEY")
'''


def send_email(user_email, name=None, role=None, message=None, subject="whitemirror page"):

    if not name:
        name = user_email
    if not message:
        message = "sin mensaje"
    if role:
        body = (
        f"Estimado {name}, en su rol como {role}, hemos recibido su mensaje y "
        "prontamente lo estaremos leyendo. Muchas gracias por su apoyo o feedback.\n\n"
        "Su mensaje fue:\n\n"
        f"{message}"
        )

    else:
        body = (
        f"Estimado {name}, hemos recibido su mensaje y "
        "prontamente lo estaremos leyendo. Muchas gracias por su apoyo o feedback.\n\n"
        "Su mensaje fue:\n\n"
        f"{message}"
        )


    msg = MIMEMultipart()
    msg['From'] = "mejorsaludmental@gmail.com" 
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())


@email_bp.route('/send', methods=['POST'])
def send_email_route():
    print(GMAIL_APP_PASSWORD)
    print(RECAPTCHA_SECRET_KEY)
    data = request.json
    user_email = data.get('user_email')
    name = data.get('name')
    role = data.get('role')
    message = data.get('message')
    subject = data.get('subject', "whitemirror page")
    captcha_token = data.get('captchaToken')

    # Ensure user_email is provided
    if not user_email:
        return jsonify({'error': 'User email is required'}), 400
    if not captcha_token:
        return jsonify({'error': 'reCAPTCHA token is required'}), 400
    recaptcha_response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': captcha_token
        }
    )
    recaptcha_result = recaptcha_response.json()

    if not recaptcha_result.get('success'):
        return jsonify({'error': 'Invalid reCAPTCHA token'}), 400

    # Call the send_email function
    try:
        send_email(user_email, name=name, role=role, message=message, subject=subject)
        return jsonify({'status': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500