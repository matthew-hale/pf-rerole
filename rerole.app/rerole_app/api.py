from flask import Blueprint, request, session, url_for, abort

from rerole_lib import character
from rerole_app import db

api = Blueprint("api", __name__, url_prefix = "/api/v0")

@api.route("/characters", methods=["GET"])
def get_characters():
    return db.get_user_characters(session["username"])

@api.route("/characters", methods=["POST"])
def create_character():
    username = session["username"]
    character_id = db.create_character(username, {})
    return {
        "id": character_id,
        "url": url_for("api.get_character", character_id=character_id),
    }, 201

@api.route("/characters/<character_id>", methods=["GET"])
def get_character(character_id: int):
    username = session["username"]
    ensure_authorized_access(username, character_id)
    data = db.get_character(character_id)
    if data is None:
        abort(404)
    return data

@api.route("/characters/<character_id>", methods=["PUT"])
def update_character(character_id: int):
    username = session["username"]
    ensure_authorized_access(username, character_id)
    data = request.json
    if data is None:
        return {"message": "Cannot create character with empty request body"}, 401

@api.route("/characters/<character_id>", methods=["DELETE"])
def delete_character(character_id: int):
    username = session["username"]
    ensure_authorized_access(username, character_id)
    db.delete_character(character_id)
    return {}, 204

@api.errorhandler(401)
def handle_401(error):
    return {"message": "Unauthorized access denied"}, 401

def ensure_authorized_access(username: str, character_id: int):
    authorized = db.user_owns_character(username, character_id)
    if not authorized:
        abort(401)
