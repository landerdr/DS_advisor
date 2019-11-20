from flask import Blueprint, request, json
import requests

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/register", methods=["POST"])
def register_user():
    post_data = request.get_json()
    response = requests.post("http://users:5000/users", json=post_data)
    return json.loads(response.content), response.status_code


@api_blueprint.route("/vehicle", methods=["POST"])
def create_vehicle():
    post_data = request.get_json()
    response = requests.post("http://vehicles:5000/vehicle", json=post_data)
    return json.loads(response.content), response.status_code


@api_blueprint.route("/vehicle", methods=["DELETE"])
def delete_vehicle():
    post_data = request.get_json()
    response = requests.delete("http://vehicles:5000/vehicle", json=post_data)
    return json.loads(response.content), response.status_code


@api_blueprint.route("/vehicle/<vehicle_id>", methods=["GET"])
def get_vehicle_info(vehicle_id):
    response = requests.get("http://vehicles:5000/vehicle/%s" % vehicle_id)
    return json.loads(response.content), response.status_code


@api_blueprint.route("/vehicle/rate", methods=["POST"])
def rate_vehicle():
    post_data = request.get_json()
    response = requests.post("http://vehicles:5000/vehicle/rate", json=post_data)
    return json.loads(response.content), response.status_code


@api_blueprint.route("/vehicle/rate", methods=["DELETE"])
def delete_vehicle_rating():
    post_data = request.get_json()
    response = requests.delete("http://vehicles:5000/vehicle/rate", json=post_data)
    return json.loads(response.content), response.status_code


@api_blueprint.route("/stop/<entity_number>/<stop_number>", methods=["GET"])
def get_stop_info(entity_number, stop_number):
    response = requests.get("http://stops:5000/stop/%d/%d" % (int(entity_number), int(stop_number)))
    return json.loads(response.content), response.status_code


@api_blueprint.route("/stop/rate", methods=["POST"])
def rate_stop():
    post_data = request.get_json()
    response = requests.post("http://stops:5000/stop/rate", json=post_data)
    return json.loads(response.content), response.status_code


@api_blueprint.route("/stop/rate", methods=["DELETE"])
def delete_stop_rating():
    post_data = request.get_json()
    response = requests.delete("http://stops:5000/stop/rate", json=post_data)
    return json.loads(response.content), response.status_code
