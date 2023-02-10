from werkzeug.exceptions import HTTPException
from app.models.pokemon import Pokemon
import pytest


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_pokemon(client):
    response = client.post("/pokemon", json={
        "name": "",
        "img_href": "Test category title",
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "pokemon" in response_body
    assert response_body == {
        "pokemon" : {
            "id": 1,
            "name": "",
            "img_href": "",
        }
    }

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_pokemon_must_contain_name(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_pokemon_must_contain_img_href(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_all_pokemon(client):
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
