from flask import Flask, Blueprint, jsonify, make_response, request
from app.models.checklist import Checklist
from app.models.category import Category
from app.utils import validate_model
from app import db, firebase

checklists_bp = Blueprint("checklists", __name__, url_prefix="/checklists")

@checklists_bp.route("", methods=["POST"])
@firebase.jwt_required
def create_checklist():
    request_body = request.get_json()
    query_param = request.args.get('category_id')
    if not "title" in request_body or not query_param:
        return make_response({"details":"Invalid submission field; missing title or category ID"}, 400)

    category = validate_model(Category, query_param)

    checklist_request_obj = request_body.copy()
    checklist_request_obj["category_id"] = category.id

    new_checklist = Checklist.from_dict(checklist_request_obj)

    db.session.add(new_checklist)
    db.session.commit()

    return {"checklist": new_checklist.to_dict()}, 201

@checklists_bp.route("", methods=["GET"])
@firebase.jwt_required
def get_all_unarchived_checklists_for_category():
    category = validate_model(Category, request.args.get("category_id"))

    all_checklists = Checklist.query.filter((Checklist.category_id == category.id) and (Checklist.is_archived == False))
    return jsonify([checklist.to_dict() for checklist in all_checklists])

@checklists_bp.route("/archive", methods=["GET"])
@firebase.jwt_required
def get_all_archived_checklists():
    all_checklists = Checklist.query.filter(Checklist.is_archived == True)
    return jsonify([checklist.to_dict() for checklist in all_checklists])

@checklists_bp.route("/favorites", methods=["GET"])
@firebase.jwt_required
def get_all_favorite_checklists():
    all_checklists = Checklist.query.filter(Checklist.is_favorited == True)
    return jsonify([checklist.to_dict() for checklist in all_checklists])

@checklists_bp.route("/<id>/archive", methods=["PATCH"])
@firebase.jwt_required
def archive_checklist(id):
    checklist = validate_model(Checklist, id)

    checklist.update_is_archived()
    db.session.commit()
    return {"checklist": checklist.to_dict()}

@checklists_bp.route("/<id>/unarchive", methods=["PATCH"])
@firebase.jwt_required
def unarchive_checklist(id):
    checklist = validate_model(Checklist, id)

    checklist.update_is_archived(False)
    db.session.commit()
    return {"checklist": checklist.to_dict()}

@checklists_bp.route("/<id>/favorite", methods=["PATCH"])
@firebase.jwt_required
def favorite_checklist(id):
    checklist = validate_model(Checklist, id)

    checklist.update_is_favorited()
    db.session.commit()
    return {"checklist": checklist.to_dict()}

@checklists_bp.route("/<id>/unfavorite", methods=["PATCH"])
@firebase.jwt_required
def unfavorite_checklist(id):
    checklist = validate_model(Checklist, id)

    checklist.update_is_favorited(False)
    db.session.commit()
    return {"checklist": checklist.to_dict()}

@checklists_bp.route("/<id>", methods=["DELETE"])
@firebase.jwt_required
def delete_checklist(id):
    checklist = validate_model(Checklist, id)

    db.session.delete(checklist)
    db.session.commit()

    return {"details": f'Checklist #{checklist.id} {checklist.title} successfully deleted'}
