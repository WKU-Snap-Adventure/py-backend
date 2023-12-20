import os
import datetime

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    # Flask Settings
    SECRET_KEY = 'mysecretkey'

    # DB Settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Settings
    JWT_SECRET_KEY = 'jwtsecretkey'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=5)