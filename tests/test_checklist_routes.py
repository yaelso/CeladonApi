from werkzeug.exceptions import HTTPException
from app.models.checklist import Checklist
from app.models.category import Category
import pytest


def test_create_checklist(client, one_category):
    response = client.post("/checklists", json={
        "title": "Test list title",
        "description": "Test list description",
        "category_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "checklist" in response_body
    assert response_body == {
        "checklist" : {
            "id": 1,
            "title": "Test list title",
            "description": "Test list description",
            "category_id": 1
        }
    }

def test_create_checklist_for_category_not_found(client):
    response = client.post("/checklists", json={
        "title": "Test list title",
        "description": "Test list description",
        "category_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Category 1 ID not found"}

def test_create_checklist_for_invalid_category(client):
    response = client.post("/checklists", json={
        "title": "Test list title",
        "description": "Test list description",
        "category_id": "x"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Category x invalid ID"}

def test_create_checklist_must_contain_title(client, one_category):
    response = client.post("/checklists", json={
        "description": "Test list description",
        "category_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Invalid submission field; missing title or category ID"}

def test_get_checklists_for_category_no_saved_checklists(client, one_category):
    response = client.get("/checklists?category_id=1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_checklists_for_category(client, one_checklist_belongs_to_one_category):
    response = client.get("/checklists?category_id=1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Automate the Boring Stuff",
            "description": "A foundational Python text",
            "category_id": 1
        }
    ]

def test_get_all_checklists_for_category_not_found(client):
    response = client.get("/checklists?category_id=1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Category 1 ID not found"}
    assert Checklist.query.all() == []

def test_get_all_checklists_for_invalid_category(client):
    response = client.get("/checklists?category_id=x")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Category x invalid ID"}
    assert Checklist.query.all() == []

def test_delete_checklist(client, one_checklist_belongs_to_one_category):
    response = client.delete("/checklists/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Checklist #1 "Automate the Boring Stuff" successfully deleted'
    }
    assert Checklist.query.get(1) == None

def test_delete_checklist_not_found(client):
    response = client.delete("/checklists/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Checklist 1 ID not found"}

def test_delete_checklist_invalid_id(client):
    response = client.delete("/checklists/x")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Checklist x invalid ID"}
