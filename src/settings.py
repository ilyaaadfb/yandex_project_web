import os
from datetime import timedelta

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(basedir, 'src/.env'))

SECRET_KEY = os.urandom(36)
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

UPLOAD_FOLDER = os.path.join(basedir, 'src', 'static', 'profile_pics', 'users')

REMEMBER_COOKIE_DURATION = timedelta(seconds=60)