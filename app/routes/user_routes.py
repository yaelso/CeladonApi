from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.user import User
from app.utils import validate_model
from app import db

users_bp = Blueprint("user", __name__, url_prefix="/user")

@users_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()
    if not "firebase_id" in request_body:
        return make_response({"details":"Invalid submission field; missing firebase_id"}, 400)

    new_user = User.from_dict(request_body)

    db.session.add(new_user)
    db.session.commit()

    return {"user": new_user.to_dict()}, 201

@users_bp.route("", methods=["GET"])
def get_all_users():
    users = User.query.all()

    return jsonify([user.to_dict() for user in users])

@users_bp.route("/<id>", methods=["GET"])
def get_user(id):
    user = validate_model(User, id)

    return {"user": user.to_dict()}

@users_bp.route("/<id>/active_pokemon", methods=["PATCH"])
def set_active_pokemon(id):
    pass

@users_bp.route("/<id>", methods=["DELETE"])
def delete_user(id):
    user = validate_model(User, id)

    db.session.delete(user)
    db.session.commit()

    return {"details": f'User #{user.id} successfully deleted'}
