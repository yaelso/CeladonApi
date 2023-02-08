from flask import Blueprint, jsonify, make_response, request
from app.models.pokemon import Pokemon
from app.utils import validate_model
from app import db, firebase

pokemon_bp = Blueprint("pokemon", __name__, url_prefix="/pokemon")

@pokemon_bp.route("", methods=["POST"])
@firebase.jwt_required
def create_pokemon():
    request_body = request.get_json()
    if not "name" in request_body or not "img_href" in request_body:
        return make_response({"details":"Invalid submission field; missing name or img_href"}, 400)

    new_pokemon = Pokemon.from_dict(request_body)

    db.session.add(new_pokemon)
    db.session.commit()

    return {"pokemon": new_pokemon.to_dict()}, 201

@pokemon_bp.route("", methods=["GET"])
@firebase.jwt_required
def get_all_pokemon():
    all_pokemon = Pokemon.query.all()

    return jsonify([pokemon.to_dict() for pokemon in all_pokemon])

@pokemon_bp.route("/<id>", methods=["DELETE"])
@firebase.jwt_required
def delete_pokemon(id):
    pokemon = validate_model(Pokemon, id)

    db.session.delete(pokemon)
    db.session.commit()

    return {"details": f'Pokemon #{pokemon.id} "{pokemon.name}" successfully deleted'}
