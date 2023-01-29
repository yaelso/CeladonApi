from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.checklist import Checklist
from app.utils import validate_model
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not "title" in request_body:
        return make_response({"details":"Invalid submission field; missing title"}, 400)

    checklist = validate_model(Checklist, request_body["checklist_id"])

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks_for_checklist():
    checklist = validate_model(Checklist, request.args.get("checklist_id"))

    all_tasks = Task.query.all()

    return jsonify([task.to_dict() for task in all_tasks])

@tasks_bp.route("/<id>", methods=["PATCH"])
def mark_task_as_completed():
    pass

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task #{task.id} "{task.title}" successfully deleted'}
