from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.checklist import Checklist
from app.utils import validate_model
from app import db, firebase

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
@firebase.jwt_required
def create_task():
    request_body = request.get_json()
    query_param = request.args.get('checklist_id')
    if not "title" in request_body or not query_param:
        return make_response({"details":"Invalid submission field; missing title or checklist ID"}, 400)

    checklist = validate_model(Checklist, query_param)

    task_request_obj = request_body.copy()
    task_request_obj["checklist_id"] = checklist.id

    new_task = Task.from_dict(task_request_obj)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
@firebase.jwt_required
def get_all_tasks_for_checklist():
    checklist = validate_model(Checklist, request.args.get("checklist_id"))

    all_tasks = Task.query.filter(Task.checklist_id == checklist.id)
    return jsonify([task.to_dict() for task in all_tasks])

@tasks_bp.route("", methods=["GET"])
@firebase.jwt_required
def get_all_tasks_for_due_date():
    due_date = request.args.get("due_date")

    all_tasks = Task.query.filter(Task.due_date == due_date)
    return jsonify([task.to_dict() for task in all_tasks])

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
@firebase.jwt_required
def mark_task_complete(id):
    task = validate_model(Task, id)

    task.update_completed_at()
    db.session.commit()
    return {"task": task.to_dict()}

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
@firebase.jwt_required
def mark_task_incomplete(id):
    task = validate_model(Task, id)

    task.update_completed_at(False)
    db.session.commit()
    return {"task": task.to_dict()}

@tasks_bp.route("/<id>/mark_in_progress", methods=["PATCH"])
@firebase.jwt_required
def mark_task_in_progress(id):
    task = validate_model(Task, id)

    task.update_in_progress()
    db.session.commit()
    return {"task": task.to_dict()}

@tasks_bp.route("/<id>/mark_not_in_progress", methods=["PATCH"])
@firebase.jwt_required
def mark_task_not_in_progress(id):
    task = validate_model(Task, id)

    task.update_in_progress(False)
    db.session.commit()
    return {"task": task.to_dict()}

@tasks_bp.route("/<id>/due_date", methods=["PATCH"])
@firebase.jwt_required
def mark_task_due_date(id):
    request_body = request.get_json()
    task = validate_model(Task, id)

    task.update_due_date(request_body["due_date"])
    db.session.commit()
    return {"task": task.to_dict()}

@tasks_bp.route("/<id>/clear_due_date", methods=["PATCH"])
@firebase.jwt_required
def clear_task_due_date(id):
    task = validate_model(Task, id)

    task.update_due_date()
    db.session.commit()
    return {"task": task.to_dict()}

@tasks_bp.route("/<id>", methods=["DELETE"])
@firebase.jwt_required
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task #{task.id} "{task.title}" successfully deleted'}
