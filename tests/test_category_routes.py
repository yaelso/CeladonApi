from werkzeug.exceptions import HTTPException
from app.models.category import Category
import pytest

from tests.conftest import HEADER


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_category(client, one_user):
    response = client.post("/categories", headers=HEADER, json={
        "user_id": 1,
        "title": "Test category title",
        "description": "Test category description"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "category" in response_body
    assert response_body == {
        "category" : {
            "id": 1,
            "user_id": 1,
            "title": "Test category title",
            "description": "Test category description"
        }
    }

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_category_must_contain_title(client, one_user):
    response = client.post("/categories", json={
        "user_id": 1,
        "description": "Test category description"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid submission field; missing title or description"
    }
    assert Category.query.all() == []

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_category_must_contain_description(client, one_user):
    response = client.post("/categories", json={
        "user_id": 1,
        "title": "Test category title"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid submission field; missing title or description"
    }
    assert Category.query.all() == []

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_categories_no_saved_categories(client, one_user):
    response = client.get("/categories", headers=HEADER)
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_all_categories(client, one_user, one_category):
    response = client.get("/categories")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "user_id": 1,
            "title": "Python Learning",
            "description": "A category devoted to Python learning resources"
        }
    ]

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_category(client, one_category):
    response = client.delete("/categories/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Category #1 "Python Learning" successfully deleted'
    }
    assert Category.query.get(1) == None

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_category_not_found(client):
    response = client.delete("/categories/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Category 1 ID not found"}

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_category_invalid_id(client):
    response = client.delete("/categories/x")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Category x invalid ID"}
