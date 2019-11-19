from flask import Blueprint, jsonify, request, json
import requests
from sqlalchemy import exc
from project.api.models import Vehicle, VehicleType, VehicleRatings
from project import db

vehicle_blueprint = Blueprint("vehicle", __name__)


@vehicle_blueprint.route("/vehicle", methods=["POST"])
def add_vehicle():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    entity_number = post_data.get("entity_number")
    vehicle_number = post_data.get("vehicle_number")
    vehicle_type = post_data.get("vehicle_type")
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        vehicle = Vehicle.query.filter_by(entity_number=entity_number, vehicle_number=vehicle_number).first()

        if not vehicle:
            response = requests.post("http://users:5000/users/login", json={"email": email, "password": password})
            if response.status_code != 200:
                response_object["message"] = "Unauthorised"
                return jsonify(response_object), 401
            r = response.json()
            db.session.add(
                Vehicle(entity_number=entity_number, vehicle_number=vehicle_number, vehicle_type=int(vehicle_type),
                        user_id=r["data"]["id"]))
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "%d %d was added" % (entity_number, vehicle_number)
            }
            return jsonify(response_object), 201
        else:
            response_object["message"] = "Sorry. That vehicle already exists."
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@vehicle_blueprint.route("/vehicle/<vehicle_id>", methods=["GET"])
def get_single_vehicle(vehicle_id):
    """Get single vehicle details"""
    response_object = {"status": "fail", "message": "Vehicle does not exist."}
    try:
        vehicle = Vehicle.query.filter_by(id=int(vehicle_id)).first()
        if not vehicle:
            return jsonify(response_object), 404
        else:
            ratings = VehicleRatings.query.filter_by(id=int(vehicle_id))
            avg = 0
            if ratings.count() != 0:
                for r in ratings:
                    avg += r.rating
                avg /= ratings.count()
            response_object = {
                "status": "success",
                "data": {
                    "id": vehicle.id,
                    "entity_number": vehicle.entity_number,
                    "vehicle_number": vehicle.vehicle_number,
                    "vehicle_type": vehicle.vehicle_type,
                    "ratings": [r.rating for r in ratings],
                    "avg_rating": avg
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@vehicle_blueprint.route("/vehicles", methods=["GET"])
def get_all_vehicles():
    response_object = {"status": "fail", "message": "There went something wrong."}
    try:
        vehicles = Vehicle.query.all()
        response_object = {
            "status": "success",
            "data": [{
                "id": vehicle.id,
                "entity_number": vehicle.entity_number,
                "vehicle_number": vehicle.vehicle_number,
                "vehicle_type": vehicle.vehicle_type
            } for vehicle in vehicles]
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@vehicle_blueprint.route("/vehicle/types", methods=["GET"])
def get_all_vehicle_types():
    response_object = {"status": "fail", "message": "There went something wrong."}
    try:
        types = VehicleType.query.all()
        response_object = {
            "status": "success",
            "data": [{
                "id": t.id,
                "vehicle_type": t.vehicle_type
            } for t in types]
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@vehicle_blueprint.route("/vehicle/rate", methods=["POST"])
def rate_vehicle():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    vehicle_id = post_data.get("vehicle_id")
    email = post_data.get("email")
    password = post_data.get("password")
    rating = post_data.get("rating")
    try:
        vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
        if vehicle:
            response = requests.post("http://users:5000/users/login", json={"email": email, "password": password})
            if response.status_code != 200:
                response_object["message"] = "Unauthorised"
                return jsonify(response_object), 401
            r = response.json()
            rate = VehicleRatings.query.filter_by(id=vehicle_id, user_id=r["data"]["id"]).first()
            if not rate:
                db.session.add(VehicleRatings(vehicle_id=vehicle_id, user_id=r["data"]["id"], rating=int(rating)))
            else:
                rate.rating = int(rating)
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Rating was added"
            }
            return jsonify(response_object), 201
        else:
            response_object["message"] = "Sorry. That vehicle doesn't exist."
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@vehicle_blueprint.route("/vehicle", methods=["DELETE"])
def delete_vehicle():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    vehicle_id = post_data.get("vehicle_id")
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
        if vehicle:
            response = requests.post("http://users:5000/users/login", json={"email": email, "password": password})
            if response.status_code != 200:
                response_object["message"] = "Unauthorised"
                return jsonify(response_object), 401
            r = response.json()
            rate = VehicleRatings.query.filter_by(id=vehicle_id)
            if not rate.count() == 0:
                response_object["message"] = "Can't remove stop that has ratings"
                return jsonify(response_object), 401
            vehicle = Vehicle.query.filter_by(id=vehicle_id, created_id=r["data"]["id"]).first()
            if not vehicle:
                response_object["message"] = "Only the account that added the stop can remove it"
                return jsonify(response_object), 401

            db.session.delete(vehicle)
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Vehicle was removed"
            }
            return jsonify(response_object), 201
        else:
            response_object["message"] = "Sorry. That vehicle doesn't exist."
            return jsonify(response_object), 400
    except ValueError:
        db.session.rollback()
        return jsonify(response_object), 400


@vehicle_blueprint.route("/vehicle/rate", methods=["DELETE"])
def delete_vehicle_rating():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    vehicle_id = post_data.get("vehicle_id")
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
        if vehicle:
            response = requests.post("http://users:5000/users/login", json={"email": email, "password": password})
            if response.status_code != 200:
                response_object["message"] = "Unauthorised"
                return jsonify(response_object), 401
            r = response.json()
            rate = VehicleRatings.query.filter_by(id=vehicle_id, user_id=r["data"]["id"]).first()
            if not rate:
                response_object["message"] = "You have not rated the vehicle"
                return jsonify(response_object), 400
            db.session.delete(rate)
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Rating was removed"
            }
            return jsonify(response_object), 201
        else:
            response_object["message"] = "Sorry. That vehicle doesn't exist."
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400
