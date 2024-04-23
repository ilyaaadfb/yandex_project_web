import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__name__))

UPLOAD_FOLDER = os.path.join(basedir, 'src', 'static', 'profile_pics', 'users')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

FLASK_ADMIN_SWATCH = 'cerulean'

SECRET_KEY = os.urandom(36)
SQLALCHEMY_DATABASE_URI = 'sqlite:///db/db.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

REMEMBER_COOKIE_DURATION = timedelta(seconds=60)
