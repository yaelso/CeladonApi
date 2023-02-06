from flask import abort, make_response, jsonify
from app.models.user import User
from app import db

def validate_model(cls, model_id):
    '''Validates model instances based on a provided model and model_id'''

    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":f"{cls.__name__} {model_id} invalid ID"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details":f"{cls.__name__} {model_id} ID not found"}, 404))

    return model

def get_user_profile_from_auth_token(token):
    '''Parses the provided JWT and returns the embedded user profile
    Currently stubbed - returns a fake profile'''

    return User.from_dict({
        "id": 1,
        "firebase_id": "Fake Test Id"
    })
