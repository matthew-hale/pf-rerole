import jwt

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request, session, url_for, abort

from rerole_lib import Sheet
from rerole_app import db

api = Blueprint("api", __name__, url_prefix = "/api/v0")
api.secret_key = "dev key"

@api.before_request
def valid_auth():
    if request.endpoint == "api.authenticate":
        return None

    auth = request.authorization
    if auth is None:
        return jsonify({
            "message": "Missing auth token.",
        }), 401

    token = auth.token
    if token is None:
        return jsonify({
            "message": "Missing auth token.",
        }), 401

    valid_token = db.valid_auth_token(token)
    if valid_token:
        db.refresh_auth_token(token)
        return None
    db.delete_auth_token(token)
    return jsonify({
        "message": "Invalid auth token.",
    }), 401

@api.after_request
def after(r):
    auth = request.authorization
    if auth is not None:
        token = auth.token
        db.refresh_auth_token(token)
    return r

@api.route("/authenticate", methods=["POST"])
def authenticate():
    auth = request.authorization
    username = auth.username
    password = auth.password
    authenticated = db.authenticate(username, password)
    if not authenticated:
        abort(401)

    method = "rerole.app"
    user_id = db.get_user_id(method, username)
    token = new_token(user_id, method, username)

    db.create_session_token(user_id, token)
    return jsonify({
        "token": token,
    }), 200

@api.route("/logout", methods=["POST"])
def logout():
    auth = request.authorization
    token = auth.token
    db.delete_auth_token(token)
    return "", 204

@api.route("/characters", methods=["GET"])
def get_characters():
    token = get_request_token()
    if not permission_to(token, "read_owned_character"):
        abort(401)

    user_id = token.get("user_id", 0)
    return jsonify(db.get_user_characters(user_id))

@api.route("/characters", methods=["POST"])
def create_character():
    token = get_request_token()
    if not permission_to(token, "create_character"):
        return jsonify({"message": "Unauthorized."}), 401
    user_id = token.get("user_id")
    data = Sheet()
    data.calculate()
    character_id = db.create_character(user_id, data)
    return jsonify({
        "id": character_id,
        "url": url_for("api.get_character", character_id=character_id),
    }), 201

@api.route("/characters/<character_id>", methods=["GET"])
def get_character(character_id: int):
    token = get_request_token()
    user_id = token.get("user_id")
    user_owns_character = db.user_owns_character(user_id, character_id)
    read_owned_character = permission_to(token, "read_owned_character")
    read_any_character = permission_to(token, "read_any_character")
    read_this_character = user_owns_character and read_owned_character
    if not (read_this_character or read_any_character):
        abort(401)

    data = db.get_character(character_id)
    if data is None:
        abort(404)
    return jsonify(data)

@api.route("/characters/<character_id>", methods=["PUT"])
def update_character(character_id: int):
    token = get_request_token()
    user_id = token.get("user_id")
    user_owns_character = db.user_owns_character(user_id, character_id)
    update_owned_character = permission_to(token, "update_owned_character")
    update_any_character = permission_to(token, "update_any_character")
    update_this_character = user_owns_character and update_owned_character
    if not (update_this_character or update_any_character):
        abort(401)

    data = Sheet(request.json)
    if data is None:
        return {"message": "Cannot update character with empty request body."}, 400
    data.calculate()
    db.update_character(character_id, data)
    return jsonify(data)

@api.route("/characters/<character_id>", methods=["DELETE"])
def delete_character(character_id: int):
    token = get_request_token()
    user_id = token.get("user_id")
    user_owns_character = db.user_owns_character(user_id, character_id)
    delete_owned_character = permission_to(token, "delete_owned_character")
    delete_any_character = permission_to(token, "delete_any_character")
    delete_this_character = user_owns_character and delete_owned_character
    if not (delete_this_character or delete_any_character):
        abort(401)

    db.delete_character(character_id)
    return {}, 204


def new_token(user_id, method, username):
    payload = {
        "user_id": user_id,
        "method": method,
        "username": username,
        "issued_at": str(datetime.now(timezone.utc)),
    }
    return jwt.encode(payload, api.secret_key, algorithm="HS256")

def get_request_token() -> dict:
    token = get_raw_request_token()
    decoded =  jwt.decode(token, api.secret_key, algorithms=["HS256"])
    if decoded is None:
        return {}
    return decoded

def get_raw_request_token() -> str:
    auth = request.authorization
    if auth is None:
        return ""
    token = auth.token
    if token is None:
        return ""
    return token

def permission_to(token, permission) -> bool:
    user_id = token.get("user_id")
    user_permissions = db.get_user_permissions(user_id)
    if isinstance(permission, str):
        return permission in user_permissions
    if isinstance(permission, list):
        return all([p in user_permissions for p in permission])

@api.errorhandler(401)
def handle_401(error):
    return {"message": "Unauthorized access denied"}, 401
