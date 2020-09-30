from flask import Blueprint, jsonify, request
# import requests
from sqlalchemy import exc
from project.api.models import StopRatings
from project import db
import requests

stops_blueprint = Blueprint("stops", __name__)


@stops_blueprint.route("/stop/rate", methods=["POST"])
def add_stop_rating():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    entity_number = post_data.get("entity_number")
    stop_number = post_data.get("stop_number")
    email = post_data.get("email")
    password = post_data.get("password")
    rating = post_data.get("rating")
    try:
        response = requests.post("http://users:5000/users/login", json={"email": email, "password": password})
        if response.status_code != 200:
            response_object["message"] = "Unauthorised"
            return jsonify(response_object), 401
        r = response.json()
        rate = StopRatings.query.filter_by(entity_number=entity_number, stop_number=stop_number,
                                           user_id=r["data"]["id"]).first()
        if not rate:
            db.session.add(
                StopRatings(entity_number=entity_number, line_number=stop_number, user_id=r["data"]["id"],
                            rating=int(rating)))
        else:
            rate.rating = int(rating)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Rating was added for %d %d" % (entity_number, stop_number)
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@stops_blueprint.route("/stop/rate", methods=["DELETE"])
def delete_stop_rating():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    entity_number = post_data.get("entity_number")
    stop_number = post_data.get("stop_number")
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        response = requests.post("http://users:5000/users/login", json={"email": email, "password": password})
        if response.status_code != 200:
            response_object["message"] = "Unauthorised"
            return jsonify(response_object), 401
        r = response.json()
        rate = StopRatings.query.filter_by(entity_number=entity_number, stop_number=stop_number,
                                           user_id=r["data"]["id"]).first()
        if not rate:
            response_object["message"] = "You have not rated the stop"
            return jsonify(response_object), 400
        db.session.delete(rate)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Rating was removed for %d %d" % (entity_number, stop_number)
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@stops_blueprint.route("/stop/<entity_number>/<stop_number>", methods=["GET"])
def get_single_vehicle(entity_number, stop_number):
    response_object = {"status": "fail", "message": "Line does not exist."}
    try:
        v = 0
        if not v:
            return jsonify(response_object), 404
        else:
            ratings = StopRatings.query.filter_by(entity_number=int(entity_number), line_number=int(stop_number))
            avg = 0
            if ratings.count() != 0:
                for r in ratings:
                    avg += r.rating
                avg /= ratings.count()
            response_object = {
                "status": "success",
                "data": {
                    "entity_number": int(entity_number),
                    "stop_number": int(stop_number),
                    "ratings": [r.rating for r in ratings],
                    "avg_rating": avg
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
