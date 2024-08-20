import json

from flask import Blueprint, render_template

from rerole_lib import character as c

site = Blueprint("site", __name__, template_folder = "templates")

with open("test_data.json") as f:
    data = c.calculate(json.load(f))

@site.route("/")
def index():
    return render_template("index.html", data=data)
