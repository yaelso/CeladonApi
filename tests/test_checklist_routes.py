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
            "category_id": 1,
            "is_archived": False,
            "is_favorited": False,
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

def test_get_unarchived_checklists_for_category_no_saved_checklists(client, one_category):
    response = client.get("/checklists?category_id=1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_unarchived_checklists_for_category(client, one_checklist_belongs_to_one_category):
    response = client.get("/checklists?category_id=1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Automate the Boring Stuff",
            "description": "A foundational Python text",
            "category_id": 1,
            "is_archived": False,
            "is_favorited": False,
        }
    ]

def test_get_all_archived_checklists_for_category(client, archived_checklist):
    response = client.get("/checklists/archive")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 2,
            "title": "Real Python - DevOps With Python",
            "description": "A Real Python learning path",
            "category_id": 1,
            "is_archived": True,
            "is_favorited": False,
        }
    ]

def test_get_all_unarchived_checklists_for_category_not_found(client):
    response = client.get("/checklists?category_id=1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Category 1 ID not found"}
    assert Checklist.query.all() == []

def test_get_all_unarchived_checklists_for_invalid_category(client):
    response = client.get("/checklists?category_id=x")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Category x invalid ID"}
    assert Checklist.query.all() == []

def test_get_all_favorited_checklists_for_category(client, favorited_checklist):
    response = client.get("/checklists/favorite")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 2,
            "title": "Real Python - DevOps With Python",
            "description": "A Real Python learning path",
            "category_id": 1,
            "is_archived": True,
            "is_favorited": True,
        }
    ]

def test_archive_checklist(client, one_checklist_belongs_to_one_category):
    response = client.patch("/checklists/1/archive")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == {
        "checklist" : {
            "id": 1,
            "title": "Automate the Boring Stuff",
            "description": "A foundational Python text",
            "category_id": 1,
            "is_archived": True,
            "is_favorited": False,
        }
    }

def test_unarchive_checklist(client, archived_checklist):
    response = client.patch("/checklists/2/unarchive")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == {
        "checklist" : {
            "id": 2,
            "title": "Real Python - DevOps With Python",
            "description": "A Real Python learning path",
            "category_id": 1,
            "is_archived": False,
            "is_favorited": False,
        }
    }

def test_favorite_checklist(client, one_checklist_belongs_to_one_category):
    response = client.patch("/checklists/1/favorite")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == {
        "checklist" : {
            "id": 1,
            "title": "Automate the Boring Stuff",
            "description": "A foundational Python text",
            "category_id": 1,
            "is_archived": True,
            "is_favorited": True,
        }
    }

def test_unfavorite_checklist(client, favorited_checklist):
    response = client.patch("/checklists/2/unfavorite")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == {
        "checklist" : {
            "id": 2,
            "title": "Real Python - DevOps With Python",
            "description": "A Real Python learning path",
            "category_id": 1,
            "is_archived": False,
            "is_favorited": False,
        }
    }

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
