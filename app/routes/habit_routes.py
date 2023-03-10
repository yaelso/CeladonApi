from flask import Blueprint, jsonify, make_response, request
from app.models.habit import Habit
from app.models.user import User
from app.utils import get_firebase_user_id, get_user_profile_from_auth_token, validate_model
from app import db

habits_bp = Blueprint("habits", __name__, url_prefix="/habits")

@habits_bp.route("", methods=["POST"])
def create_habit():
    request_body = request.get_json()
    if not "title" in request_body:
        return make_response({"details":"Invalid submission field; missing title"}, 400)

    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    user = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()

    habit_request_obj = request_body.copy()
    habit_request_obj["user_id"] = user.id

    new_habit = Habit.from_dict(habit_request_obj)

    db.session.add(new_habit)
    db.session.commit()

    return {"habit": new_habit.to_dict()}, 201

@habits_bp.route("", methods=["GET"])
def get_all_habits():
    firebase_user_id = get_firebase_user_id(
        get_user_profile_from_auth_token(request.headers["Authorization"])
    )

    user = User.query.filter(User.firebase_id == firebase_user_id).one_or_none()

    all_habits = Habit.query.filter(Habit.user_id == user.id)

    return jsonify([habit.to_dict() for habit in all_habits])

@habits_bp.route("/<id>/update_reps", methods=["PATCH"])
def update_reps(id):
    request_body = request.get_json()
    habit = validate_model(Habit, id)

    habit.update_reps(request_body["reps"])
    db.session.commit()
    return {"habit": habit.to_dict()}

@habits_bp.route("/<id>/reset_reps", methods=["PATCH"])
def reset_reps(id):
    habit = validate_model(Habit, id)

    habit.reset_reps()
    db.session.commit()
    return {"habit": habit.to_dict()}

@habits_bp.route("/<id>", methods=["DELETE"])
def delete_habit(id):
    habit = validate_model(Habit, id)

    db.session.delete(habit)
    db.session.commit()

    return {"details": f'Habit #{habit.id} {habit.title} successfully deleted'}
