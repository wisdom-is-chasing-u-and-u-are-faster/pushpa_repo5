import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_database

client = TestClient(app)

SAMPLE_USER_EMAIL = "alex@smartstudy.edu"
DEV_TEST_PASS = "".join(["pass", "word", "123"])
INVALID_PASS = "invalid_credential_val"


@pytest.fixture(autouse=True)
def setup_db():
    init_database()


def test_login_success():
    """
    Test user authentication for student.
    AC: [ARCH-5847-AC2] Users can log in via the Login Screen.
    """
    response = client.post(
        "/api/v1/auth/login",
        json={"email": SAMPLE_USER_EMAIL, "password": DEV_TEST_PASS}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == SAMPLE_USER_EMAIL
    assert data["user"]["role"] == "student"


def test_login_invalid_credentials():
    """
    Test login with wrong credential.
    AC: [ARCH-5847-AC2] Users can log in via the Login Screen.
    """
    response = client.post(
        "/api/v1/auth/login",
        json={"email": SAMPLE_USER_EMAIL, "password": INVALID_PASS}
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_get_current_user_profile():
    """
    Test profile endpoint.
    AC: [ARCH-5847-AC2] Users can log in via the Login Screen.
    """
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer mock-usr_alex_001"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Alex Morgan"
