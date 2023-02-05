from werkzeug.exceptions import HTTPException
from app.models.user_pokemon import UserPokemon
import pytest


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_all_user_pokemon(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_user_pokemon(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_user_pokemon_must_contain_user_id(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_user_pokemon_must_contain_pokemon_id(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_update_user_pokemon_exp(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_reset_user_pokemon_exp(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_user_pokemon(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_user_pokemon_not_found(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_user_pokemon_invalid_id(client):
    pass
