from app import db

from .model import BagItem

from . import blue as app

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

# Get the items in the bag
@app.route("/items", methods=["GET"])
@jwt_required()
def get_items():
    # Get items
    items = current_user.items
    # Return response
    return jsonify({"msg": "Items retrieved", "items": [{"item_name": item.item_name, "count": item.count} for item in items]}), 200

# Add an item to the bag
@app.route("/items", methods=["POST"])
@jwt_required()
def add_item():
    # Get item_name and count from request
    item_name = request.json.get("item_name", None)
    count = request.json.get("count", None)
    # Check if item_name and count exist
    if not item_name:
        return jsonify({"msg": "Missing item_name parameter"}), 400
    if not count:
        return jsonify({"msg": "Missing count parameter"}), 400
    # Create new item
    item = BagItem.query.filter_by(user_id=current_user.id, item_name=item_name).one_or_none()
    if item is not None:
        item.count += count
    else:
        item = BagItem(user_id=current_user.id, item_name=item_name, count=count)
        db.session.add(item)
    db.session.commit()
    # Return response
    return jsonify({"msg": "Item added", "count": item.count}), 201

# Remove certain number of item from the bag
@app.route("/items", methods=["DELETE"])
@jwt_required()
def remove_item():
    # Get item_name and count from request
    item_name = request.json.get("item_name", None)
    count = request.json.get("count", None)
    # Check if item_name and count exist
    if not item_name:
        return jsonify({"msg": "Missing item_name parameter"}), 400
    if not count:
        return jsonify({"msg": "Missing count parameter"}), 400
    # Get item from database
    item = BagItem.query.filter_by(user_id=current_user.id, item_name=item_name).one_or_none()
    # Check if item exist
    if item is None:
        return jsonify({"msg": "Item not found"}), 404
    # Check if count is valid
    if item.count < count:
        return jsonify({"msg": "No enough item"}), 400
    # Update count
    item.count -= count
    if item.count == 0:
        db.session.delete(item)
    db.session.commit()
    # Return response
    return jsonify({"msg": "Item removed", "count": item.count}), 200