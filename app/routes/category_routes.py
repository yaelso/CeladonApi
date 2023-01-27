from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.category import Category
from app.utils import validate_model
from app import db

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

@categories_bp.route("", methods=["POST"])
def create_category():
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details":"Invalid submission field"}, 400)

    new_category= Category.from_dict(request_body)

    db.session.add(new_category)
    db.session.commit()

    return {"category": new_category.to_dict()}, 201

@categories_bp.route("", methods=["GET"])
def get_all_categories():
    categories = Category.query.all()

    return jsonify([category.to_dict() for category in categories])

@categories_bp.route("/<id>", methods=["DELETE"])
def delete_category(id):
    category = validate_model(Category, id)

    db.session.delete(category)
    db.session.commit()

    return {"details": f'Category #{category.id} "{category.title}" successfully deleted'}
