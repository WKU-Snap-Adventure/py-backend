from app import db
from app.baidu_aip import objectDetect
from app.bag.model import BagItem
from .model import CollectRule

from . import blue as app

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

# Receive an image from client
# Return the collected item
@app.route("/image", methods=["POST"])
@jwt_required()
def collect_item():
    # Get image from request
    image = request.files.get("file", None).read()
    # Check if image exist
    if not image:
        return jsonify({"msg": "Missing image parameter"}), 400
    # Perform image recognization
    result = objectDetect(image).get("result", [])
    if len(result) == 0:
        return jsonify({"msg": "No item detected"}), 400
    # Get the corresponding rule
    output = []
    for item in result:
        item_name = item.get("keyword", None)
        if not item_name:
            continue
        rules = CollectRule.query.filter_by(item_name=item_name).all()
        for rule in rules:
            output.append(rule.calculte_rule())
        if len(output) > 0:
            break
    if len(output) == 0:
        return jsonify({"msg": "No rule matched"}), 400
    # Save the collected item
    for item in output:
        item_name = item.get("item_name", None)
        count = item.get("count", None)
        # Create new item
        item = BagItem.query.filter_by(user_id=current_user.id, item_name=item_name).one_or_none()
        if item is not None:
            item.count += count
        else:
            item = BagItem(user_id=current_user.id, item_name=item_name, count=count)
            db.session.add(item)
        db.session.commit()
    # Return response
    return jsonify({"msg": "Item collected", "item": item_name, "product": output}), 200