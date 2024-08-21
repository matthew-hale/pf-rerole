import os
import secrets
from urllib.parse import urlencode

import requests
from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from rerole_app.db import delete_session, refresh_session

from rerole_lib import character as c

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

@site.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("site.login"))
    refresh_session(session["username"], session["token"])
    return render_template("index.html", username=session["username"])

@site.route("/login")
def login():
    if "username" in session:
        return redirect(url_for("site.index"))
    return render_template("login.html")

@site.route("/logout")
def logout():
    username = session.get("username")
    token = session.get("token")
    delete_session(username, token)
    if "username" in session:
        del session["username"]
    if "token" in session:
        del session["token"]
    return redirect(url_for("site.index"))

@site.route("/authorize/<provider>")
def oauth2_authorize(provider):
    if "username" in session:
        return redirect(url_for("site.index"))

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
    if "username" in session:
        return redirect(url_for("site.index"))

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

    session["username"] = email
    session["token"] = secrets.token_urlsafe(16)
    refresh_session(session["username"], session["token"])
    return redirect(url_for("site.index"))
