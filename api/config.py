from dotenv import dotenv_values
from keys import CHATBOT_SECRET_KEY, CHATBOT_DATABASE_URI

# Load environment variables from .env file into a dictionary
env_config = dotenv_values(".env")

class Config:
    SECRET_KEY = CHATBOT_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = CHATBOT_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    TALISMAN_CSP = {
        'default-src': '\'self\''
        # Add more CSP policies as needed
    }
    TALISMAN_FORCE_HTTPS = True
    TALISMAN_FRAME_OPTIONS = 'DENY'
