from flask.cli import FlaskGroup
from flask import Flask, json, jsonify
import requests
import os

app = Flask(__name__)
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)
cli = FlaskGroup(app)


class DeLijnRequests:
    def __init__(self):
        self.header = {
            "Ocp-Apim-Subscription-Key": "16dc01a8d7374c239ee2fb185689fb60"}
        self.base_url = "https://api.delijn.be/DLKernOpenData/api/v1"

    def get(self, endpoint):
        return requests.get(self.base_url + endpoint, headers=self.header)


cache = {}


@app.route("/lines", methods=["GET"])
def get_all_lines():
    if "lines" in cache:
        return jsonify({"status": "success", "data": cache["lines"]}), 200
    response = DeLijnRequests().get("/lijnen")
    response_object = {"status": "fail", "message": "DL failed"}
    if response.status_code != 200:
        return jsonify(response_object), 400
    r = response.json()
    keys = ["%d_%d" % (int(line["entiteitnummer"]), int(line["lijnnummer"])) for line in r["lijnen"]]
    cache["lines"] = []
    for i in range(0, len(keys), 10):
        response = DeLijnRequests().get("/lijnen/lijst/%s/lijnrichtingen" % "_".join(keys[i:min(i + 10, len(keys))]))
        if response.status_code != 200:
            cache.pop("lines")
            return jsonify(response_object), 400
        r = response.json()
        for lines in r["lijnLijnrichtingen"]:
            for line in lines["lijnrichtingen"]:
                cache["lines"].append({"entity_number": line["entiteitnummer"], "line_number": line["lijnnummer"],
                                       "direction": line["richting"], "description": line["omschrijving"]})
    return jsonify({"status": "success", "data": cache["lines"]}), 200


@app.route("/stops", methods=["GET"])
def get_all_stops():
    if "stops" in cache:
        return jsonify({"status": "success", "data": cache["stops"]}), 200
    response_object = {"status": "fail", "message": "DL failed"}
    response = DeLijnRequests().get("/haltes")
    if response.status_code != 200:
        return jsonify(response_object), 400
    r = response.json()
    cache["stops"] = [{"entity_number": stop["entiteitnummer"], "stop_number": stop["haltenummer"]} for stop in
                      r["haltes"]]
    return jsonify({"status": "success", "data": cache["stops"]}), 200


@app.route("/towns", methods=["GET"])
def get_all_towns():
    response = DeLijnRequests().get("/gemeenten")
    response_object = {"status": "fail", "message": "DL failed"}
    if response.status_code != 200:
        return jsonify(response_object), 400
    r = response.json()
    response_object = {"status": "success",
                       "data": [{"id": town["gemeentenummer"], "town": town["omschrijving"]}
                                for town in r["gemeenten"]]}
    return jsonify(response_object), 200


@app.route("/town/<town_id>/stops", methods=["GET"])
def get_all_stops_from_town(town_id):
    response = DeLijnRequests().get("/gemeenten/%d/haltes" % int(town_id))
    response_object = {"status": "fail", "message": "DL failed"}
    if response.status_code != 200:
        return jsonify(response_object), 400
    r = response.json()
    response_object = {"status": "success",
                       "data": [{"entity_number": stop["entiteitnummer"], "stop_number": stop["haltenummer"]} for stop
                                in r["haltes"]]}
    return jsonify(response_object), 200


@app.route("/line/<entity_number>/<line_number>/<direction>/stops", methods=["GET"])
def get_all_stops_from_line(entity_number, line_number, direction):
    response = DeLijnRequests().get(
        "/lijnen/%d/%d/lijnrichtingen/%s/haltes" % (int(entity_number), int(line_number), direction))
    response_object = {"status": "fail", "message": "DL failed"}
    if response.status_code != 200:
        return jsonify(response_object), 400
    r = response.json()
    response_object = {"status": "success",
                       "data": [{"entity_number": stop["entiteitnummer"], "stop_number": stop["haltenummer"]} for stop
                                in r["haltes"]]}
    return jsonify(response_object), 200


if __name__ == "__main__":
    cli()
