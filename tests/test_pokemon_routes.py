from werkzeug.exceptions import HTTPException
from app.models.pokemon import Pokemon
import pytest


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_all_pokemon(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_pokemon(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_pokemon_must_contain_name(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_pokemon_must_contain_img_href(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_pokemon(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_pokemon_not_found(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_pokemon_invalid_id(client):
    pass
