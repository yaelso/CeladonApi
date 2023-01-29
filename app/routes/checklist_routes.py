from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.checklist import Checklist
from app.models.category import Category
from app.utils import validate_model
from app import db

checklists_bp = Blueprint("checklists", __name__, url_prefix="/checklists")

@checklists_bp.route("", methods=["POST"])
def create_checklist():
    request_body = request.get_json()
    if not "title" in request_body or not "category_id" in request_body:
        return make_response({"details":"Invalid submission field; missing title or category ID"}, 400)

    category = validate_model(Category, request_body["category_id"])

    new_checklist = Checklist.from_dict(request_body)

    db.session.add(new_checklist)
    db.session.commit()

    return {"checklist": new_checklist.to_dict()}, 201

@checklists_bp.route("", methods=["GET"])
def get_all_checklists_for_category():
    category = validate_model(Category, request.args.get("category_id"))

    all_checklists = Checklist.query.filter(Checklist.category_id == category.id)
    return jsonify([checklist.to_dict() for checklist in all_checklists])

@checklists_bp.route("/<id>", methods=["PATCH"])
def archive_checklist():
    pass

@checklists_bp.route("/<id>", methods=["DELETE"])
def delete_checklist(id):
    checklist = validate_model(Checklist, id)

    db.session.delete(checklist)
    db.session.commit()

    return {"details": f'Checklist #{checklist.id} "{checklist.title}" successfully deleted'}
