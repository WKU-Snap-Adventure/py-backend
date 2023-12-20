# Create Buleprint
from flask import Blueprint
blue = Blueprint("collect", __name__, url_prefix="/collect")

# Add routes
from . import api