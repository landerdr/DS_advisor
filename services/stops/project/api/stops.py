from flask import Blueprint, jsonify, request
# import requests
from sqlalchemy import exc
from project.api.models import StopRatings
from project import db
import requests

lines_blueprint = Blueprint("stops", __name__)


@lines_blueprint.route("/stop/rate", methods=["POST"])
def add_vehicle():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    entity_number = post_data.get("entity_number")
    stop_number = post_data.get("stop_number")
    user_id = post_data.get("user_id")
    rating = post_data.get("rating")
    try:
        rate = StopRatings.query.filter_by(entity_number=entity_number, stop_number=stop_number,
                                           user_id=user_id).first()
        if not rate:
            db.session.add(
                StopRatings(entity_number=entity_number, line_number=stop_number, user_id=user_id, rating=rating))
        else:
            rate.rating = rating
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Rating was added for %d %d" % (entity_number, stop_number)
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@lines_blueprint.route("/stop/<entity_number>/<stop_number>", methods=["GET"])
def get_single_vehicle(entity_number, stop_number):
    response_object = {"status": "fail", "message": "Line does not exist."}
    try:
        v = 0
        if not v:
            return jsonify(response_object), 404
        else:
            ratings = StopRatings.query.filter_by(entity_number=int(entity_number), line_number=int(stop_number))
            response_object = {
                "status": "success",
                "data": {
                    "entity_number": int(entity_number),
                    "stop_number": int(stop_number),
                    "ratings": [r.rating for r in ratings]
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
