from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# SUCCESS CASES

def test_get_all_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_task():
    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_create_task():

    new_task = {
        "id": 10,
        "title": "Learn GitHub Actions",
        "description": "Setup CI workflow",
        "status": "Pending",
        "priority": "High"
    }

    response = client.post("/tasks", json=new_task)

    assert response.status_code == 201
    assert response.json()["title"] == "Learn GitHub Actions"


def test_update_task():

    updated_task = {
        "id": 1,
        "title": "Complete Assignment Updated",
        "description": "Finish and submit",
        "status": "Completed",
        "priority": "High"
    }

    response = client.put("/tasks/1", json=updated_task)

    assert response.status_code == 200
    assert response.json()["status"] == "Completed"


def test_delete_task():

    response = client.delete("/tasks/2")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


# INVALID SCENARIOS

def test_get_nonexistent_task():

    response = client.get("/tasks/999")

    assert response.status_code == 404


def test_create_duplicate_task():

    duplicate_task = {
        "id": 1,
        "title": "Duplicate",
        "description": "Duplicate task",
        "status": "Pending",
        "priority": "Low"
    }

    response = client.post("/tasks", json=duplicate_task)

    assert response.status_code == 400


def test_update_nonexistent_task():

    updated_task = {
        "id": 999,
        "title": "Unknown",
        "description": "Unknown task",
        "status": "Pending",
        "priority": "Low"
    }

    response = client.put("/tasks/999", json=updated_task)

    assert response.status_code == 404


def test_update_task_id_mismatch():

    updated_task = {
        "id": 5,
        "title": "Mismatch",
        "description": "Wrong ID",
        "status": "Pending",
        "priority": "Low"
    }

    response = client.put("/tasks/1", json=updated_task)

    assert response.status_code == 400


def test_delete_nonexistent_task():

    response = client.delete("/tasks/999")

    assert response.status_code == 404