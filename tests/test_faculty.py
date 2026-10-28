import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    init_database()


def test_faculty_overview_metrics():
    """
    Test faculty overview aggregate metrics.
    AC: [ARCH-5847-AC4] Faculty can view student progress on the Faculty Dashboard.
    """
    response = client.get("/api/v1/faculty/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_students"] >= 4
    assert data["class_average_velocity"] > 0
    assert data["at_risk_students_count"] >= 1


def test_faculty_students_roster():
    """
    Test faculty student roster and at-risk detection.
    AC: [ARCH-5847-AC4] Faculty can view student progress on the Faculty Dashboard.
    """
    response = client.get("/api/v1/faculty/students")
    assert response.status_code == 200
    data = response.json()
    assert "students" in data
    assert len(data["students"]) >= 4
    # David Kim should be identified as At-Risk
    david = next((s for s in data["students"] if "David" in s["name"]), None)
    assert david is not None
    assert david["at_risk"] is True
