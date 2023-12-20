from app import db
from app.user.model import User

from . import blue as app

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

# Receive an image from client
# Return the collected item
@app.route("/image", methods=["POST"])
@jwt_required()
def collect_item():
    # Get image from request
    image = request.files.get("file", None)
    # Check if image exist
    if not image:
        return jsonify({"msg": "Missing image parameter"}), 400
    # Get user
    user = User.query.filter_by(id=current_user.id).one_or_none()
    # Collect item
    item = user.collect_item(image)
    # Return response
    return jsonify({"msg": "Item collected", "item": item}), 200