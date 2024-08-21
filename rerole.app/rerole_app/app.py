from flask import Flask, session

from rerole_app.api import api
from rerole_app.db import init
from rerole_app.site import site

app = Flask(__name__)
app.register_blueprint(site)
app.register_blueprint(api)

app.json.sort_keys = False

app.secret_key = "dev key"

init()
