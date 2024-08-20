from flask import Flask
from rerole_app.site import site

app = Flask(__name__)
app.register_blueprint(site)
