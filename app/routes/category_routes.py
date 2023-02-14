from flask import Blueprint, jsonify, make_response, request
from app.models.category import Category
from app.models.user import User
from app.utils import get_firebase_user_id, get_user_profile_from_auth_token, validate_model
from app import db, firebase

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

@categories_bp.route("", methods=["POST"])
@firebase.jwt_required
def create_category():
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details":"Invalid submission field; missing title or description"}, 400)

    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    user = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()

    category_request_obj = request_body.copy()
    category_request_obj["user_id"] = user.id

    new_category = Category.from_dict(category_request_obj)

    db.session.add(new_category)
    db.session.commit()

    return {"category": new_category.to_dict()}, 201

@categories_bp.route("", methods=["GET"])
@firebase.jwt_required
def get_all_categories():
    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    categories = Category.query.join(User).filter(User.firebase_id == firebase_user_id)

    return jsonify([category.to_dict(category.checklists) for category in categories])

@categories_bp.route("/<id>", methods=["DELETE"])
@firebase.jwt_required
def delete_category(id):
    category = validate_model(Category, id)

    db.session.delete(category)
    db.session.commit()

    return {"details": f'Category #{category.id} {category.title} successfully deleted'}
