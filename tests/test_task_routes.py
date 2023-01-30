from werkzeug.exceptions import HTTPException
from app.models.task import Task
import pytest


def test_create_task(client, one_checklist_belongs_to_one_category):
    response = client.post("/tasks", json={
        "title": "Test task title",
        "checklist_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task" : {
            "id": 1,
            "title": "Test task title",
            "checklist_id": 1,
            "is_complete": False,
            "in_progress": False,
            "due_date": None,
        }
    }

def test_create_task_for_checklist_not_found(client):
    response = client.post("/tasks", json={
        "title": "Test task title",
        "checklist_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Checklist 1 ID not found"}

def test_create_task_for_invalid_checklist(client):
    response = client.post("/tasks", json={
        "title": "Test task title",
        "checklist_id": "x"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Checklist x invalid ID"}

def test_create_task_must_contain_title(client, one_checklist_belongs_to_one_category):
    response = client.post("/tasks", json={
        "checklist_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid submission field; missing title"
    }
    assert Task.query.all() == []

def test_get_tasks_for_checklist_no_saved_tasks(client, one_checklist_belongs_to_one_category):
    response = client.get("/tasks?checklist_id=1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_tasks_for_checklist(client, three_tasks_belong_to_one_checklist):
    response = client.get("/tasks?checklist_id=1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Chapter 1",
            "checklist_id": 1,
            "is_complete": False,
            "in_progress": False,
            "due_date": None,
        },
        {
            "id": 2,
            "title": "Chapter 2",
            "checklist_id": 1,
            "is_complete": False,
            "in_progress": False,
            "due_date": None,
        },
        {
            "id": 3,
            "title": "Chapter 3",
            "checklist_id": 1,
            "is_complete": False,
            "in_progress": False,
            "due_date": None,
        }
    ]

def test_get_all_tasks_for_checklist_not_found(client):
    response = client.get("/tasks?checklist_id=1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Checklist 1 ID not found"}
    assert Task.query.all() == []

def test_get_all_tasks_for_invalid_checklist(client):
    response = client.get("/tasks?checklist_id=x")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Checklist x invalid ID"}
    assert Task.query.all() == []

def test_mark_task_as_complete(client, one_task_belong_to_one_checklist):
    response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == { "task": {
        "id": 1,
        "title": "Chapter 1",
        "checklist_id": 1,
        "is_complete": True,
        "in_progress": False,
        "due_date": None,
    }}

def test_mark_complete_task_as_incomplete(client, one_task_belong_to_one_checklist):
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == { "task": {
        "id": 1,
        "title": "Chapter 1",
        "checklist_id": 1,
        "is_complete": False,
        "in_progress": False,
        "due_date": None,
    }}

def test_mark_task_as_in_progress(client, one_task_belong_to_one_checklist):
    response = client.patch("/tasks/1/mark_in_progress")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == { "task": {
        "id": 1,
        "title": "Chapter 1",
        "checklist_id": 1,
        "is_complete": False,
        "in_progress": True,
        "due_date": None,
    }}

def test_mark_task_as_not_in_progress(client, one_task_belong_to_one_checklist):
    response = client.patch("/tasks/1/mark_not_in_progress")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == { "task": {
        "id": 1,
        "title": "Chapter 1",
        "checklist_id": 1,
        "is_complete": False,
        "in_progress": False,
        "due_date": None,
    }}

def test_delete_task(client, one_task_belong_to_one_checklist):
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Task #1 "Chapter 1" successfully deleted'
    }
    assert Task.query.get(1) == None

def test_delete_task_not_found(client):
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Task 1 ID not found"}

def test_delete_task_invalid_id(client):
    response = client.delete("/tasks/x")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Task x invalid ID"}
