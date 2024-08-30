import os
import secrets
from urllib.parse import urlencode

import requests
from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from rerole_app import db
from rerole_app import api

site = Blueprint("site", __name__, template_folder = "templates")

OAUTH2_CONFIG = {
    "github": {
        "client_id": os.environ.get("PF_REROLE_GITHUB_CLIENT_ID"),
        "client_secret": os.environ.get("PF_REROLE_GITHUB_CLIENT_SECRET"),
        "authorize_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo": {
            "url": "https://api.github.com/user/emails",
            "email": lambda json: json[0]["email"],
        },
        "scopes": ["user:email"],
    },
}

_anonymous_endpoints = [
    "site.login",
    "site.logout",
    "site.oauth2_authorize",
    "site.oauth2_callback",
]
@site.before_request
def before():
    if "user_id" in session:
        return None
    if request.endpoint in _anonymous_endpoints:
        return None

    return redirect(url_for("site.login"))

@site.route("/")
def index():
    token = session.pop("token", "")
    return render_template("index.html", token=token)

@site.route("/characters/<character_id>")
def character(character_id: int):
    return render_template("character.html", character_id=character_id)

@site.route("/login")
def login():
    return render_template("login.html")

@site.route("/logout")
def logout():
    if "token" in session:
        token = session.pop("token", None)
        db.delete_auth_token(token)
    if "user_id" in session:
        del session["user_id"]
    return redirect(url_for("site.index"))

@site.route("/authorize/<provider>")
def oauth2_authorize(provider):
    provider_data = OAUTH2_CONFIG.get(provider)
    if provider_data is None:
        abort(404)

    session["oauth2_state"] = secrets.token_urlsafe(16)

    query_string = urlencode({
        "client_id": provider_data["client_id"],
        "redirect_uri": url_for("site.oauth2_callback", provider=provider, _external=True),
        "response_type": "code",
        "scope": " ".join(provider_data["scopes"]),
        "state": session["oauth2_state"],
    })

    return redirect(provider_data["authorize_url"] + "?" + query_string)

@site.route("/callback/<provider>")
def oauth2_callback(provider):
    provider_data = OAUTH2_CONFIG.get(provider)
    if provider_data is None:
        abort(404)

    if "error" in request.args:
        return redirect(url_for("site.index"))

    mismatched_state = request.args["state"] != session.get("oauth2_state")
    missing_auth_code = "code" not in request.args

    if mismatched_state or missing_auth_code:
        abort(401)

    response = requests.post(provider_data["token_url"], data={
        "client_id": provider_data["client_id"],
        "client_secret": provider_data["client_secret"],
        "code": request.args["code"],
        "grant_type": "authorization_code",
        "redirect_uri": url_for("site.oauth2_callback", provider=provider, _external=True),
    }, headers={"Accept": "application/json"})

    response_error = response.status_code != 200
    oauth2_token = response.json().get("access_token")
    no_token = not oauth2_token

    if response_error or no_token:
        abort(401)

    response = requests.get(provider_data["userinfo"]["url"], headers={
        "Authorization": "Bearer " + oauth2_token,
        "Accept": "application/json",
    })

    response_error = response.status_code != 200

    if response_error:
        abort(401)

    email = provider_data["userinfo"]["email"](response.json())

    if db.user_exists(provider, email):
        user_id = db.get_user_id(provider, email)
    else:
        user_id = db.create_user(provider, email)
    if user_id is None:
        abort(401)

    token = api.new_token(user_id, provider, email)
    db.create_session_token(user_id, token)
    session["user_id"] = user_id
    session["token"] = token
    return redirect(url_for("site.index"))
