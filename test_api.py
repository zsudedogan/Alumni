"""
Automated unit tests for Week 03 classroom routes.
Run with: pytest test_api.py
"""

import pytest
import uuid

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


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_20_register_user_with_role_and_department():
    """Verify user registration with specific ecosystem role and department"""
    import uuid
    unique_email = f"alumni_{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "Baris Akarsu",
        "email": unique_email,
        "password": "secretpassword123",
        "role": "Alumni",
        "department": "Computer Engineering",
        "age": 27,
        "bio": "Senior Cloud Engineer at TechCorp"
    }

    # Register user
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Baris Akarsu"
    assert data["email"] == unique_email
    assert data["role"] == "Alumni"
    assert data["department"] == "Computer Engineering"
    assert data["bio"] == "Senior Cloud Engineer at TechCorp"
    assert "password" not in data  # Ensure security sanitization
    user_id = data["id"]

    # Verify user is retrievable via GET /api/users/{id}
    get_res = client.get(f"/api/users/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json()["role"] == "Alumni"

    # Duplicate registration should fail with 400
    dup_res = client.post("/api/auth/register", json=payload)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"].lower()


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_21_register_user_validation_checks():
    """Verify validation rules: minimum password length and allowed roles"""
    import uuid
    # 1. Short password (< 6 chars)
    short_pw_payload = {
        "name": "Short Pw User",
        "email": f"short_{uuid.uuid4().hex[:6]}@example.com",
        "password": "123",
        "role": "Student"
    }
    res_short = client.post("/api/auth/register", json=short_pw_payload)
    assert res_short.status_code == 400
    assert "at least 6 characters" in res_short.json()["detail"]

    # 2. Invalid role
    invalid_role_payload = {
        "name": "Hacker User",
        "email": f"hacker_{uuid.uuid4().hex[:6]}@example.com",
        "password": "password123",
        "role": "SuperAdminGodMode"
    }
    res_role = client.post("/api/auth/register", json=invalid_role_payload)
    assert res_role.status_code == 400
    assert "invalid role" in res_role.json()["detail"].lower()


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_22_register_web_view():
    """Verify registration HTML web view is accessible and renders role choices"""
    res = client.get("/register/")
    assert res.status_code == 200
    assert "text/html" in res.headers.get("content-type", "")
    assert "Join Alumni Ecosystem" in res.text
    assert "Student" in res.text
    assert "Alumni" in res.text
    assert "Recruiter" in res.text
    assert "Academic" in res.text
    assert "Select Your Role" in res.text


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_23_auth_middleware_blocks_unauthenticated_admin_access():
    """Verify AuthMiddleware blocks unauthenticated requests to /admin/ and /api/admin"""
    # 1. Web HTML request: redirects to login
    res_web = client.get("/admin/", headers={"Accept": "text/html"}, follow_redirects=False)
    assert res_web.status_code == 303
    assert "/login/" in res_web.headers.get("location", "")

    # 2. JSON API request: returns 401 Unauthorized
    res_api = client.delete("/api/admin/users/999", headers={"Accept": "application/json"})
    assert res_api.status_code == 401
    assert "authentication required" in res_api.json()["detail"].lower()


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_24_auth_login_and_session_flow():
    """Verify login authentication endpoint sets cookie and returns session token"""
    # 1. Invalid credentials
    res_bad = client.post("/api/auth/login", json={"email": "sude@example.com", "password": "wrongpassword"})
    assert res_bad.status_code == 401
    assert "invalid email or password" in res_bad.json()["detail"].lower()

    # 2. Valid credentials (Sude Dogan)
    res_good = client.post("/api/auth/login", json={"email": "sude@example.com", "password": "password123"})
    assert res_good.status_code == 200
    data = res_good.json()
    assert "token" in data
    assert data["user"]["email"] == "sude@example.com"
    assert data["user"]["role"] == "Admin"

    # Verify session cookie was set
    token = data["token"]
    assert token.startswith("sess_")

    # 3. /api/auth/me with Bearer token
    res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    assert res_me.json()["name"] == "Sude Dogan"


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_25_admin_panel_access_and_rbac():
    """Verify RBAC: non-admin gets 403 Forbidden, Admin gets 200 OK dashboard"""
    import uuid
    # 1. Register and login as a normal Student
    student_email = f"student_{uuid.uuid4().hex[:6]}@example.com"
    reg_res = client.post("/api/auth/register", json={
        "name": "Normal Student",
        "email": student_email,
        "password": "password123",
        "role": "Student"
    })
    assert reg_res.status_code == 201

    login_student = client.post("/api/auth/login", json={"email": student_email, "password": "password123"})
    student_token = login_student.json()["token"]

    # Student trying to access /admin/: gets 403 Forbidden
    res_forbidden = client.get(
        "/admin/",
        headers={"Accept": "text/html", "Authorization": f"Bearer {student_token}"}
    )
    assert res_forbidden.status_code == 403
    assert "403" in res_forbidden.text or "Yönetici Yetkisi Gerekli" in res_forbidden.text

    # 2. Admin (Sude Dogan) accessing /admin/: gets 200 OK
    login_admin = client.post("/api/auth/login", json={"email": "sude@example.com", "password": "password123"})
    admin_token = login_admin.json()["token"]

    res_admin = client.get(
        "/admin/",
        headers={"Accept": "text/html", "Authorization": f"Bearer {admin_token}"}
    )
    assert res_admin.status_code == 200
    assert "UniBridge Yönetim Paneli" in res_admin.text
    assert "Sude Dogan" in res_admin.text


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_26_admin_data_manipulation():
    """Verify Admin can manipulate data: change user role, publish announcement, delete announcement"""
    # Login as Admin
    login_admin = client.post("/api/auth/login", json={"email": "sude@example.com", "password": "password123"})
    admin_token = login_admin.json()["token"]
    cookies = {"session_token": admin_token}

    # 1. Admin creates a user
    res_create_user = client.post(
        "/admin/users/create",
        data={"name": "Test Stajyer", "email": f"staj_{uuid.uuid4().hex[:6]}@example.com", "role": "Student", "department": "YBS", "password": "password123"},
        cookies=cookies,
        follow_redirects=False
    )
    assert res_create_user.status_code == 303

    # 2. Admin creates an announcement
    res_ann = client.post(
        "/admin/announcements/create",
        data={"title": "Admin Test Duyurusu", "content": "Sistem admin paneli testi.", "category": "Kariyer"},
        cookies=cookies,
        follow_redirects=False
    )
    assert res_ann.status_code == 303

    # Verify announcement is listed
    res_list = client.get("/announcements/")
    assert "Admin Test Duyurusu" in res_list.text

    # 3. Admin updates role of user 1 to Admin
    res_role = client.post(
        "/admin/users/1/role",
        data={"role": "Admin"},
        cookies=cookies,
        follow_redirects=False
    )
    assert res_role.status_code == 303


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_27_dynamic_navigation_menu_by_role():
    """Verify navigation menu adapts dynamically depending on the user's role"""
    # 1. Guest navigation (ensure fresh unauthenticated client state)
    client.cookies.clear()
    res_guest = client.get("/", headers={"Accept": "text/html"})
    assert res_guest.status_code == 200
    assert "Giriş" in res_guest.text
    assert "Register" in res_guest.text or "Kayıt Ol" in res_guest.text

    # 2. Student navigation
    client.cookies.clear()
    student_email = f"nav_student_{uuid.uuid4().hex[:6]}@example.com"
    client.post("/api/auth/register", json={
        "name": "Sude Ogr",
        "email": student_email,
        "password": "password123",
        "role": "Student"
    })
    login_student = client.post("/api/auth/login", json={"email": student_email, "password": "password123"}).json()
    token_student = login_student["token"]

    res_student = client.get("/", headers={"Authorization": f"Bearer {token_student}"})
    assert res_student.status_code == 200
    assert "Öğrenci Portalı" in res_student.text
    assert "Başvurularım" in res_student.text
    assert "Sude Ogr" in res_student.text

    # 3. Admin navigation
    client.cookies.clear()
    login_admin = client.post("/api/auth/login", json={"email": "sude@example.com", "password": "password123"}).json()
    token_admin = login_admin["token"]

    res_admin = client.get("/", headers={"Authorization": f"Bearer {token_admin}"})
    assert res_admin.status_code == 200
    assert "Admin Paneli" in res_admin.text


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_28_user_specific_portal_pages():
    """Verify tailored portal views for Student, Alumni, Recruiter, and Academic roles"""
    client.cookies.clear()
    # 1. Student Portal
    res_student = client.get("/portal/student")
    assert res_student.status_code == 200
    assert "Öğrenci Portalı" in res_student.text
    assert "Başvuru Takip Çizelgesi" in res_student.text

    # 2. Alumni Portal
    res_alumni = client.get("/portal/alumni")
    assert res_alumni.status_code == 200
    assert "Mezun Portalı" in res_alumni.text
    assert "Mezun Mentorluk" in res_alumni.text

    # 3. Recruiter Portal
    res_recruiter = client.get("/portal/recruiter")
    assert res_recruiter.status_code == 200
    assert "İşveren Portalı" in res_recruiter.text
    assert "Yetenek Havuzu" in res_recruiter.text

    # 4. Academic Portal
    res_academic = client.get("/portal/academic")
    assert res_academic.status_code == 200
    assert "Akademik Portal" in res_academic.text
    assert "Bölüm Öğrenci & Mezunları" in res_academic.text

    # 5. Universal /portal/ router redirects unauthenticated to login
    client.cookies.clear()
    res_portal_redirect = client.get("/portal/", follow_redirects=False)
    assert res_portal_redirect.status_code == 303
    assert "/login/" in res_portal_redirect.headers.get("location", "")




