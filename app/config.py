from .jobs.auth_basic import HTTPBasicAuth
import os
from distutils.util import strtobool
from dotenv import load_dotenv
load_dotenv() 

class Config:
    """App configuration."""
    DEBUG = strtobool(os.getenv('DEBUG', 'True'))
    SCHEDULER_API_ENABLED = strtobool(os.getenv('SCHEDULER_API_ENABLED', 'True'))
    SCHEDULER_AUTH = HTTPBasicAuth()
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = strtobool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'True'))
    SECRET_KEY = os.getenv('SECRET_KEY')
    GOOGLE_CLOUD_CREDENTIAL = os.getenv('GOOGLE_CLOUD_CREDENTIAL')