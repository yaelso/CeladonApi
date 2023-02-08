from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.user_pokemon import UserPokemon
from app.models.user import User
from app.utils import get_firebase_user_id, get_user_profile_from_auth_token, validate_model
from app import db, firebase

user_pokemon_bp = Blueprint("user_pokemon", __name__, url_prefix="/user_pokemon")

@user_pokemon_bp.route("", methods=["POST"])
@firebase.jwt_required
def create_user_pokemon():
    request_body = request.get_json()
    if not "user_id" in request_body or not "pokemon_id" in request_body:
        return make_response({"details":"Invalid submission field; missing title or description"}, 400)

    user = get_user_profile_from_auth_token(request.headers["Authorization"])

    user_pokemon_request_obj = request_body.copy()
    user_pokemon_request_obj["user_id"] = user.id

    new_user_pokemon = UserPokemon.from_dict(user_pokemon_request_obj)

    db.session.add(new_user_pokemon)
    db.session.commit()

    return {"user pokemon": new_user_pokemon.to_dict()}, 201

@user_pokemon_bp.route("", methods=["GET"])
@firebase.jwt_required
def get_all_user_pokemon():
    user = get_user_profile_from_auth_token(request.headers['Authorization'])
    user_pokemon = UserPokemon.query.filter(UserPokemon.user_id == user.id)

    return jsonify([pokemon.to_dict() for pokemon in user_pokemon])

@user_pokemon_bp.route("/<id>/exp", methods=["PATCH"])
@firebase.jwt_required
def update_user_pokemon_exp(id):
    request_body = request.get_json()
    user_pokemon = validate_model(UserPokemon, id)

    user_pokemon.update_exp(request_body["exp"])
    db.session.commit()
    return {"user pokemon": user_pokemon.to_dict()}

@user_pokemon_bp.route("/<id>/reset_exp", methods=["PATCH"])
@firebase.jwt_required
def reset_user_pokemon_exp(id):
    user_pokemon = validate_model(UserPokemon, id)

    user_pokemon.reset_exp()
    db.session.commit()
    return {"user pokemon": user_pokemon.to_dict()}
