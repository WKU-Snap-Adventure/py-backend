# Create Buleprint
from flask import Blueprint
blue = Blueprint("user", __name__, url_prefix="/user")

# Add routes
from . import api