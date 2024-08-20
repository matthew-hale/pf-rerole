import json

from flask import Flask

app = Flask(__name__)
with open("test_data.json") as f:
    data = json.load(f)

@app.route("/")
def index():
    return data
