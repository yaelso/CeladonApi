from flask import Blueprint, jsonify, make_response, request
from app.models.user_pokemon import UserPokemon
from app.models.user import User
from app.utils import get_firebase_user_id, get_user_profile_from_auth_token
from app import db, firebase

user_pokemon_bp = Blueprint("user_pokemon", __name__, url_prefix="/user_pokemon")

@user_pokemon_bp.route("", methods=["POST"])
@firebase.jwt_required
def create_user_pokemon():
    query_param = request.args.get('pokemon_id')

    if not query_param:
        return make_response({"details":"Invalid submission field; missing Pokemon ID"}, 400)

    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    user = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()

    user_pokemon_request_obj = {}
    user_pokemon_request_obj["user_id"] = user.id
    user_pokemon_request_obj["pokemon_id"] = query_param

    new_user_pokemon = UserPokemon.from_dict(user_pokemon_request_obj)

    db.session.add(new_user_pokemon)
    db.session.commit()

    return {"user pokemon": new_user_pokemon.to_dict()}, 201

@user_pokemon_bp.route("", methods=["GET"])
@firebase.jwt_required
def get_all_user_pokemon():
    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    user = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()

    user_pokemon = UserPokemon.query.filter(UserPokemon.user_id == user.id)

    return jsonify([pokemon.to_dict(pokemon.pokemon) for pokemon in user_pokemon])

@user_pokemon_bp.route("/<id>/exp", methods=["PATCH"])
@firebase.jwt_required
def update_user_pokemon_exp(id):
    request_body = request.get_json()
    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    user = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()
    pokemon = UserPokemon.query.get({"user_id": user.id, "pokemon_id": id})

    pokemon.update_exp(request_body["exp"])
    db.session.commit()
    return {"user pokemon": pokemon.to_dict()}

@user_pokemon_bp.route("/<id>/reset_exp", methods=["PATCH"])
@firebase.jwt_required
def reset_user_pokemon_exp(id):
    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    user = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()
    pokemon = UserPokemon.query.get({"user_id": user.id, "pokemon_id": id})

    pokemon.reset_exp()
    db.session.commit()
    return {"user pokemon": pokemon.to_dict()}
