from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.user import User
from app.utils import get_firebase_user_id, get_user_profile_from_auth_token, validate_model
from app import db, firebase

users_bp = Blueprint("user", __name__, url_prefix="/user")

@users_bp.route("", methods=["POST"])
@firebase.jwt_required
def create_user():
    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    exists = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()

    if exists != None:
        return make_response({"details":"User already exists"}, 400)

    new_user = User.from_dict(firebase_user_id)

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
    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )
    user = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()

    if not user:
        abort(make_response({"details":f"User not found"}, 404))

    request_body = request.get_json()

    user.update_active_pokemon(request_body["active_pokemon_id"])

    db.session.commit()

    return {"user": user.to_dict}

@users_bp.route("/<id>", methods=["DELETE"])
@firebase.jwt_required
def delete_user(id):
    user = validate_model(User, id)

    db.session.delete(user)
    db.session.commit()

    return {"details": f'User #{user.id} successfully deleted'}
