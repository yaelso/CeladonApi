from werkzeug.exceptions import HTTPException
from app.models.user import User
import pytest


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_user(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_user_must_contain_firebase_id(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_all_users(client, three_users):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_user(client, one_user):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_update_active_pokemon_no_active_pokemon(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_update_active_pokemon_with_already_active_pokemon(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_user(client, one_user):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_user_not_found(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_user_invalid_id(client):
    pass
