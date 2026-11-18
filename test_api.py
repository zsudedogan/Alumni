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


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_11_direct_applications_crud():
    # First, ensure we have a job posting to reference
    job_payload = {
        "title": "Test App Position",
        "company": "AppTest Corp",
        "description": "Position for application testing",
    }
    job_res = client.post("/api/job-postings", json=job_payload)
    assert job_res.status_code == 201
    job_id = job_res.json()["id"]

    # Direct CREATE application
    app_payload = {
        "job_id": job_id,
        "user_id": 1,
        "resume_url": "https://linkedin.com/in/testuser",
        "cover_note": "Very motivated candidate",
        "status": "Pending"
    }
    create_res = client.post("/api/applications", json=app_payload)
    assert create_res.status_code == 201
    app_data = create_res.json()
    app_id = app_data["id"]
    assert app_data["job_id"] == job_id
    assert app_data["user_id"] == 1
    assert app_data["status"] == "Pending"

    # Direct READ ALL
    list_res = client.get("/api/applications")
    assert list_res.status_code == 200
    assert any(a["id"] == app_id for a in list_res.json())

    # Direct READ ALL with filter
    filter_res = client.get(f"/api/applications?job_id={job_id}")
    assert filter_res.status_code == 200
    assert all(a["job_id"] == job_id for a in filter_res.json())

    # Direct READ BY ID (with details)
    get_res = client.get(f"/api/applications/{app_id}")
    assert get_res.status_code == 200
    detail = get_res.json()
    assert detail["id"] == app_id
    assert "applicant_name" in detail
    assert "job_title" in detail

    # Direct PATCH (update status)
    patch_res = client.patch(f"/api/applications/{app_id}", json={"status": "Reviewed"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "Reviewed"

    # Direct DELETE
    del_res = client.delete(f"/api/applications/{app_id}")
    assert del_res.status_code == 200
    assert client.get(f"/api/applications/{app_id}").status_code == 404

    # Cleanup job posting
    client.delete(f"/api/job-postings/{job_id}")


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_12_nested_job_applications():
    # Create a job posting first
    job_payload = {
        "title": "Nested Test Internship",
        "company": "NestedTest Inc",
        "description": "Testing nested application routes",
    }
    job_res = client.post("/api/job-postings", json=job_payload)
    assert job_res.status_code == 201
    job_id = job_res.json()["id"]

    # Nested CREATE: POST /api/job-postings/{job_id}/applications
    nested_payload = {
        "user_id": 1,
        "resume_url": "https://github.com/testuser",
        "cover_note": "Nested route application test"
    }
    create_res = client.post(f"/api/job-postings/{job_id}/applications", json=nested_payload)
    assert create_res.status_code == 201
    app_data = create_res.json()
    app_id = app_data["id"]
    assert app_data["job_id"] == job_id

    # Nested READ ALL: GET /api/job-postings/{job_id}/applications
    list_res = client.get(f"/api/job-postings/{job_id}/applications")
    assert list_res.status_code == 200
    assert any(a["id"] == app_id for a in list_res.json())

    # Nested READ SINGLE: GET /api/job-postings/{job_id}/applications/{app_id}
    get_res = client.get(f"/api/job-postings/{job_id}/applications/{app_id}")
    assert get_res.status_code == 200
    assert get_res.json()["job_id"] == job_id

    # Nested 404 for non-existent job
    assert client.get("/api/job-postings/99999/applications").status_code == 404

    # Nested DELETE: DELETE /api/job-postings/{job_id}/applications/{app_id}
    del_res = client.delete(f"/api/job-postings/{job_id}/applications/{app_id}")
    assert del_res.status_code == 200

    # Cleanup job posting
    client.delete(f"/api/job-postings/{job_id}")


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_13_nested_user_applications():
    # Create a job posting first
    job_payload = {
        "title": "User Nested Test Role",
        "company": "UserNest Corp",
        "description": "Testing user nested application routes",
    }
    job_res = client.post("/api/job-postings", json=job_payload)
    assert job_res.status_code == 201
    job_id = job_res.json()["id"]

    # Nested CREATE: POST /api/users/1/applications
    user_app_payload = {
        "job_id": job_id,
        "cover_note": "User nested application test"
    }
    create_res = client.post("/api/users/1/applications", json=user_app_payload)
    assert create_res.status_code == 201
    app_data = create_res.json()
    app_id = app_data["id"]
    assert app_data["user_id"] == 1

    # Nested READ ALL: GET /api/users/1/applications
    list_res = client.get("/api/users/1/applications")
    assert list_res.status_code == 200
    user_app_ids = [a["id"] for a in list_res.json()]
    assert app_id in user_app_ids

    # Nested READ SINGLE: GET /api/users/1/applications/{app_id}
    get_res = client.get(f"/api/users/1/applications/{app_id}")
    assert get_res.status_code == 200
    assert get_res.json()["user_id"] == 1

    # Nested 404 for non-existent user
    assert client.get("/api/users/99999/applications").status_code == 404

    # Nested DELETE: DELETE /api/users/1/applications/{app_id}
    del_res = client.delete(f"/api/users/1/applications/{app_id}")
    assert del_res.status_code == 200

    # Cleanup job posting
    client.delete(f"/api/job-postings/{job_id}")


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_14_applications_web_view():
    res = client.get("/applications/")
    assert res.status_code == 200
    assert "Student Job Applications" in res.text


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_15_job_posting_title_max_120_validation():
    """Verify that title exceeding 120 characters is rejected with 400 validation failed"""
    long_title = "A" * 121
    payload = {
        "title": long_title,
        "company": "Validation Test Co"
    }
    res = client.post("/api/job-postings", json=payload)
    assert res.status_code == 400
    data = res.json()
    assert data["error"] == "validation failed"
    assert "detail" in data


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_16_job_posting_optional_city_and_description():
    """Verify that JobPosting succeeds with city and optional description"""
    payload = {
        "title": "Backend Intern",
        "company": "FastAPI Labs",
        "city": "Izmir"
    }
    res = client.post("/api/job-postings", json=payload)
    assert res.status_code == 201
    job = res.json()
    assert job["title"] == "Backend Intern"
    assert job["company"] == "FastAPI Labs"
    assert job["city"] == "Izmir"
    assert job["description"] is None

    # Cleanup
    client.delete(f"/api/job-postings/{job['id']}")


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_17_malformed_json_body_check():
    """Verify that malformed JSON body returns HTTP 400 with 'validation failed'"""
    res = client.post(
        "/api/users",
        content='{"name": "Broken JSON", "age": }',
        headers={"Content-Type": "application/json"}
    )
    assert res.status_code == 400
    data = res.json()
    assert data["error"] == "validation failed"
    assert "malformed or invalid json" in data["reason"].lower()


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_18_404_guardian_json_and_html_with_reason():
    """Verify 404 Guardian returns structured reason in JSON and HTML"""
    # 1. API 404 JSON
    api_res = client.get("/api/non-existent-endpoint")
    assert api_res.status_code == 404
    json_data = api_res.json()
    assert json_data["error"] == "Not Found"
    assert "reason" in json_data
    assert json_data["path"] == "/api/non-existent-endpoint"

    # 2. Web 404 HTML
    web_res = client.get("/non-existent-web-page", headers={"Accept": "text/html"})
    assert web_res.status_code == 404
    assert "404 GUARDIAN" in web_res.text
    assert "Reason:" in web_res.text


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_19_error_logging_mechanism():
    """Verify that errors are recorded in logs/error.logs"""
    import os
    from middlewares.logger import ERROR_LOG_FILE

    # Trigger a 404 error
    client.get("/api/trigger-log-test-404")

    # Assert error log file exists and has content
    assert os.path.exists(ERROR_LOG_FILE)
    with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
        log_content = f.read()
    assert "/api/trigger-log-test-404" in log_content

