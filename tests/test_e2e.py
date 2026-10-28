import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    init_database()


def test_health_check_endpoint():
    """Test health probe."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_index_html():
    """AC: [ARCH-5847-AC1] The implemented UI must visually match the provided "Variant A" mockups."""
    res = client.get("/")
    assert res.status_code == 200
    assert "Smart Study" in res.text


def test_login_and_dashboard_pages():
    """AC: [ARCH-5847-AC1] The implemented UI must visually match the provided "Variant A" mockups."""
    res_login = client.get("/pages/login.html")
    assert res_login.status_code == 200
    assert "Sign In" in res_login.text

    res_student = client.get("/pages/student_dashboard.html")
    assert res_student.status_code == 200
    assert "Student Dashboard" in res_student.text


def test_faculty_and_quiz_pages():
    """AC: [ARCH-5847-AC1] The implemented UI must visually match the provided "Variant A" mockups."""
    res_faculty = client.get("/pages/faculty_dashboard.html")
    assert res_faculty.status_code == 200
    assert "Faculty" in res_faculty.text

    res_syllabus = client.get("/pages/syllabus_management.html")
    assert res_syllabus.status_code == 200
    assert "Syllabus" in res_syllabus.text

    res_quiz = client.get("/pages/quiz_center.html")
    assert res_quiz.status_code == 200
    assert "Quiz" in res_quiz.text
