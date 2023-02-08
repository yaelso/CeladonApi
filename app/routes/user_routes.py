from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.user import User
from app.utils import get_firebase_user_id, get_user_profile_from_auth_token, validate_model
from app import db, firebase

users_bp = Blueprint("user", __name__, url_prefix="/user")

@users_bp.route("", methods=["POST"])
@firebase.jwt_required
def create_user():
    request_body = request.get_json()
    if not "firebase_id" in request_body:
        return make_response({"details":"Invalid submission field; missing firebase_id"}, 400)

    new_user = User.from_dict(request_body)

    db.session.add(new_user)
    db.session.commit()

    return {"user": new_user.to_dict()}, 201

@users_bp.route("", methods=["GET"])
@firebase.jwt_required
def get_all_users():
    users = User.query.all()

    return jsonify([user.to_dict() for user in users])

@users_bp.route("/<id>", methods=["GET"])
@firebase.jwt_required
def get_user(id):
    user = validate_model(User, id)

    return {"user": user.to_dict()}

@users_bp.route("/active_pokemon", methods=["PATCH"])
@firebase.jwt_required
def set_active_pokemon():
    user_from_token = get_user_profile_from_auth_token(request.headers["Authorization"])
    user_from_db = User.query.filter(User.id == user_from_token.id).one_or_none()

    if not user_from_db:
        abort(make_response({"details":f"User not found"}, 404))

    request_body = request.get_json()

    user_from_db.update_active_pokemon(request_body["active_pokemon_id"])

    db.session.commit()

    return {"user": user_from_db.to_dict}

@users_bp.route("/<id>", methods=["DELETE"])
@firebase.jwt_required
def delete_user(id):
    user = validate_model(User, id)

    db.session.delete(user)
    db.session.commit()

    return {"details": f'User #{user.id} successfully deleted'}
