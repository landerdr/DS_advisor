from flask.cli import FlaskGroup
from flask import Flask, render_template, json
from api import api_blueprint
import requests
import os

app = Flask(__name__)
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)
cli = FlaskGroup(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/vehicles", methods=["GET"])
def vehicles():
    v = requests.get("http://vehicles:5000/vehicles")
    t = requests.get("http://vehicles:5000/vehicle/types")
    types = {}
    for vt in t.json()["data"]:
        types[int(vt["id"])] = vt["vehicle_type"]
    return render_template("vehicles.html", vehicles=json.loads(v.content), types=types)


@app.route("/stops", methods=["GET"])
def stops():
    lines = requests.get("http://dlproxy:5000/lines")
    towns = requests.get("http://dlproxy:5000/towns")
    return render_template("stops.html", lines=lines.json(), towns=towns.json())


@app.route("/stops/all", methods=["GET"])
def all_stops():
    s = requests.get("http://dlproxy:5000/stops")
    return render_template("rate_stop.html", stops=s.json())


@app.route("/stops/town/<town_id>", methods=["GET"])
def all_stops_from_town(town_id):
    s = requests.get("http://dlproxy:5000/town/%d/stops" % int(town_id))
    return render_template("rate_stop.html", stops=s.json())


@app.route("/stops/line/<entity_number>/<line_number>/<direction>", methods=["GET"])
def all_stops_from_line(entity_number, line_number, direction):
    s = requests.get("http://dlproxy:5000/line/%d/%d/%s/stops" % (int(entity_number), int(line_number), direction))
    return render_template("rate_stop.html", stops=s.json())


@app.route("/users", methods=["GET"])
def users():
    return render_template("users.html")


app.register_blueprint(api_blueprint)


if __name__ == "__main__":
    cli()
