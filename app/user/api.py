from app import db
from app.user.model import User

from . import blue as app

from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user

@app.route("/login", methods=["POST"])
def login():
    # Get username and password from request
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Check if username and password exist
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = User.query.filter_by(username=username).one_or_none()
    # Check if user exist and password is correct
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401
    # Successfully login, create access token
    access_token = create_access_token(identity=user)
    # Return access token
    response = jsonify(
        access_token=access_token,
        nickname=user.nickname
        )
    # Set cookie (alternative way to store access token)
    response.set_cookie("access_token_cookie", access_token)
    # Return response
    return response, 200

@app.route("/register", methods=["POST"])
def register():
    # Get username and password from request
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    nickname = request.json.get("nickname", None)
    # Check if username and password exist
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    # Check if username already exist
    if User.query.filter_by(username=username).one_or_none():
        return jsonify({"msg": "Username already exist"}), 400
    # Create new user
    user = User(username=username, password=password, nickname=nickname)
    db.session.add(user)
    db.session.commit()
    # Return response
    return jsonify({"msg": "User created"}), 201

@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    # Return response
    return jsonify(
        username=current_user.username,
        nickname=current_user.nickname
        ), 200

@app.route("/profile", methods=["PUT"])
@jwt_required()
def update_nickname():
    # Get user from database
    user = current_user
    # Get new nickname from request
    nickname = request.json.get("nickname", None)
    # Check if nickname exist
    if not nickname:
        return jsonify({"msg": "Missing nickname parameter"}), 400
    # Update nickname
    user.nickname = nickname
    db.session.commit()
    # Return response
    return jsonify({"msg": "User updated"}), 200

@app.route("/profile", methods=["DELETE"])
@jwt_required()
def delete_user():
    # Get user from database
    user = current_user
    # Delete user
    db.session.delete(user)
    db.session.commit()
    # Return response
    return jsonify({"msg": "User deleted"}), 200

@app.route("/password", methods=["PUT"])
@jwt_required()
def update_password():
    # Get user from database
    user = current_user
    # Get password from request
    password = request.json.get("password", None)
    # Check if password exist
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    # Update password
    user.password = password
    db.session.commit()
    # Return response
    return jsonify({"msg": "Password updated"}), 200