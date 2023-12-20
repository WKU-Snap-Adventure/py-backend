# Create Buleprint
from flask import Blueprint
blue = Blueprint("bag", __name__, url_prefix="/bag")

# Add routes
from . import api