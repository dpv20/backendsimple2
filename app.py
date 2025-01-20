import os
from flask import Flask
from flask_cors import CORS
from api.email.send_email import email_bp  # Import the email blueprint
from dotenv import load_dotenv


load_dotenv()
GMAIL_APP_PASSWORD = os.getenv("APP_MAIL_PASS")
RECAPTCHA_SECRET_KEY = os.getenv("CAPTCHA_SECRET_KEY")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
if not GMAIL_APP_PASSWORD:
    raise EnvironmentError("APP_MAIL_PASS is not set in the environment or .env file.")
if not RECAPTCHA_SECRET_KEY:
    raise EnvironmentError("CAPTCHA_SECRET_KEY is not set in the environment or .env file.")
if not GMAIL_ADDRESS:
    raise EnvironmentError("GMAIL_ADDRESS is not set in the environment or .env file.")

# Load configuration settings from config.py
def create_app():
    app = Flask(__name__)
    #INSEGURO!
    CORS(app, resources={r"/*": {"origins": ['http://localhost:3000','https://whitemirror.cl', 'http://whitemirror.cl','http://ec2-3-142-160-157.us-east-2.compute.amazonaws.com/']}})
    #CORS(app)
    # Load the configuration from the Config class in config.py
    app.config.from_object('config.Config')

    # Register the email blueprint
    app.register_blueprint(email_bp, url_prefix='/api/email')

    return app

if __name__ == '__main__':
    app = create_app()
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=80, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()
  
    # Enable CORS for the frontend to access the backend
    #CORS(app, resources={r"/*": {"origins": ['http://localhost:3000', 'http://localhost:3002', 'http://ec2-3-142-160-157.us-east-2.compute.amazonaws.com/']}})
    #CORS(app)
    app.run(host='0.0.0.0', port=port, debug=True)
