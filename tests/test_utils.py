from werkzeug.exceptions import HTTPException
from app.utils import get_user_profile_from_auth_token
import pytest

PERSON_ATTR_NAME = 'person'

def test_get_user_profile_from_auth_token():
    # Token segments:
    # Here's some text!.{ "person": "Yael" }.Here's some more text!
    auth_str = 'Bearer SGVyZSdzIHNvbWUgdGV4dCEK.eyAicGVyc29uIjogIllhZWwiIH0K.SGVyZSdzIHNvbWUgbW9yZSB0ZXh0IQo='
    decoded_str = get_user_profile_from_auth_token(auth_str)
    assert decoded_str[PERSON_ATTR_NAME] == 'Yael'
