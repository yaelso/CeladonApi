from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.user_pokemon import UserPokemon
from app.utils import validate_model
from app import db

user_pokemon_bp = Blueprint("user_pokemon", __name__, url_prefix="/user_pokemon")

@user_pokemon_bp.route("", methods=["POST"])
def create_user_pokemon():
    request_body = request.get_json()
    if not "user_id" in request_body or not "pokemon_id" in request_body:
        return make_response({"details":"Invalid submission field; missing title or description"}, 400)

    new_user_pokemon = UserPokemon.from_dict(request_body)

    db.session.add(new_user_pokemon)
    db.session.commit()

    return {"user pokemon": new_user_pokemon.to_dict()}, 201

@user_pokemon_bp.route("", methods=["GET"])
def get_all_user_pokemon():
    user_pokemon = UserPokemon.query.all()

    return jsonify([pokemon.to_dict() for pokemon in user_pokemon])

@user_pokemon_bp.route("/<id>/exp", methods=["PATCH"])
def update_user_pokemon_exp(id):
    request_body = request.get_json()
    user_pokemon = validate_model(UserPokemon, id)

    user_pokemon.update_exp(request_body["exp"])
    db.session.commit()
    return {"user pokemon": user_pokemon.to_dict()}

@user_pokemon_bp.route("/<id>/reset_exp", methods=["PATCH"])
def reset_user_pokemon_exp(id):
    user_pokemon = validate_model(UserPokemon, id)

    user_pokemon.reset_exp()
    db.session.commit()
    return {"user pokemon": user_pokemon.to_dict()}
