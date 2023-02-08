from flask import abort, make_response, jsonify
from app.models.user import User
from app import db
from collections import namedtuple
import json
import base64

FIREBASE_USER_ID_ATTR_NAME = 'user_id'

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

def get_user_profile_from_auth_token(auth_str):
    '''Parses the provided JWT and returns the embedded user profile'''

    _, token = auth_str.split()
    _, profile_base64, _ = token.split('.')
    profile_json = base64.b64decode(profile_base64 + '==')
    return json.loads(profile_json)

def get_firebase_user_id(profile):
    return profile[FIREBASE_USER_ID_ATTR_NAME]
