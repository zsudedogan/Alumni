"""
Automated unit tests for Week 03 classroom routes.
Run with: pytest test_api.py
"""

import pytest

try:
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
except ImportError:
    client = None


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_1_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_3_post_create_user():
    new_user_payload = {"name": "Canan Ozturk", "age": 24, "email": "canan@example.com"}
    response = client.post("/api/users", json=new_user_payload)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["name"] == "Canan Ozturk"
    assert created_user["age"] == 24
    assert "id" in created_user


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_4_get_list_all_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 2


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_4b_get_user_by_id():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert "name" in user


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_4b_get_user_by_id_not_found():
    response = client.get("/api/users/99999")
    assert response.status_code == 404


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_5_put_update_user():
    put_payload = {"name": "Emre Updated", "age": 25, "email": "emre.new@example.com"}
    response = client.put("/api/users/1", json=put_payload)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "Emre Updated"
    assert updated_user["age"] == 25


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_5_patch_update_user():
    patch_payload = {"age": 26}
    response = client.patch("/api/users/1", json=patch_payload)
    assert response.status_code == 200
    patched_user = response.json()
    assert patched_user["age"] == 26
    assert patched_user["name"] == "Emre Updated"  # Unchanged field remains


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_6_delete_user():
    # First create a temp user to delete
    create_res = client.post("/api/users", json={"name": "Temp Delete", "age": 30})
    user_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/users/{user_id}")
    assert delete_res.status_code == 200

    # Ensure it's gone
    get_res = client.get(f"/api/users/{user_id}")
    assert get_res.status_code == 404


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_7_swagger_endpoint():
    response = client.get("/api/swagger")
    assert response.status_code == 200
