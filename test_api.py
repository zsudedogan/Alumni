"""
Automated unit tests for the whiteboard routes.
Can be run with pytest: pytest test_api.py
"""

import pytest

try:
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
except ImportError:
    client = None


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_route_1_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "ok"


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_route_2_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.text == "Hello, World!"


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_route_3_hello_name():
    response = client.get("/hello/emre")
    assert response.status_code == 200
    assert response.text == "Hello, Emre!"


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_route_4_sum():
    response = client.get("/sum/12/8")
    assert response.status_code == 200
    data = response.json()
    assert data["sum"] == 20
    assert data["number1"] == 12
    assert data["number2"] == 8


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_route_5_temporary_main_page():
    response = client.get("/main")
    assert response.status_code == 200
    assert "Temporary Main Page" in response.text


@pytest.mark.skipif(client is None, reason="FastAPI or TestClient not installed yet")
def test_alumni_endpoints():
    get_res = client.get("/alumni")
    assert get_res.status_code == 200
    initial_count = len(get_res.json())

    post_res = client.post(
        "/alumni",
        json={"full_name": "Can Kaya", "department": "EE", "graduation_year": 2021}
    )
    assert post_res.status_code == 201
    assert post_res.json()["full_name"] == "Can Kaya"

    updated_res = client.get("/alumni")
    assert len(updated_res.json()) == initial_count + 1
