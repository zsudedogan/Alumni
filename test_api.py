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


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_8_direct_job_postings_crud():
    # Direct CREATE
    payload = {
        "title": "Full Stack Python Engineer",
        "company": "NextGen Soft",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "FastAPI and Vue.js engineering",
        "salary_range": "$2,500"
    }
    create_res = client.post("/api/job-postings", json=payload)
    assert create_res.status_code == 201
    job = create_res.json()
    job_id = job["id"]

    # Direct READ ALL
    list_res = client.get("/api/job-postings")
    assert list_res.status_code == 200
    assert any(j["id"] == job_id for j in list_res.json())

    # Direct READ BY ID
    get_res = client.get(f"/api/job-postings/{job_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Full Stack Python Engineer"

    # Direct PATCH
    patch_res = client.patch(f"/api/job-postings/{job_id}", json={"salary_range": "$3,000"})
    assert patch_res.status_code == 200
    assert patch_res.json()["salary_range"] == "$3,000"

    # Direct DELETE
    del_res = client.delete(f"/api/job-postings/{job_id}")
    assert del_res.status_code == 200
    assert client.get(f"/api/job-postings/{job_id}").status_code == 404


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_9_nested_user_job_postings():
    # Nested CREATE under User 1
    nested_payload = {
        "title": "Machine Learning Intern",
        "company": "DeepMind Campus Partner",
        "location": "Istanbul",
        "job_type": "Internship",
        "description": "Assist with transformer model evaluations."
    }
    create_res = client.post("/api/users/1/job-postings", json=nested_payload)
    assert create_res.status_code == 201
    job = create_res.json()
    job_id = job["id"]
    assert job["user_id"] == 1

    # Nested READ ALL for User 1
    list_res = client.get("/api/users/1/job-postings")
    assert list_res.status_code == 200
    user_job_ids = [j["id"] for j in list_res.json()]
    assert job_id in user_job_ids

    # Nested READ SINGLE under User 1
    get_res = client.get(f"/api/users/1/job-postings/{job_id}")
    assert get_res.status_code == 200
    assert get_res.json()["user_id"] == 1

    # Nested 404 for non-existent user
    assert client.get("/api/users/9999/job-postings").status_code == 404

    # Nested DELETE under User 1
    del_res = client.delete(f"/api/users/1/job-postings/{job_id}")
    assert del_res.status_code == 200


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_10_job_postings_web_view():
    res = client.get("/job-postings/")
    assert res.status_code == 200
    assert "Career Portal & Job Postings" in res.text

