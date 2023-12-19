from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from config import Config

# Create App
app = Flask(__name__)

# Load Config
app.config.from_object(Config)

# Load Extensions
jwt = JWTManager(app)
db = SQLAlchemy(app)
bc = Bcrypt(app)

# Load Blueprints
from app.user import blue as userblue
app.register_blueprint(userblue)

# Create Database
with app.app_context():
    db.create_all()