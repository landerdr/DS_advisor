from flask.cli import FlaskGroup
from flask import Flask, render_template, json
from api import api_blueprint
import requests
import os

app = Flask(__name__)
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)
cli = FlaskGroup(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/vehicles")
def vehicles():
    v = requests.get("http://vehicles:5000/vehicles")
    t = requests.get("http://vehicles:5000/vehicle/types")
    types = {}
    for vt in t.json()["data"]:
        types[int(vt["id"])] = vt["vehicle_type"]
    return render_template("vehicles.html", vehicles=json.loads(v.content), types=types)


@app.route("/stops")
def stops():
    return render_template("stops.html")


@app.route("/users")
def users():
    return render_template("users.html")


app.register_blueprint(api_blueprint)


if __name__ == "__main__":
    cli()
