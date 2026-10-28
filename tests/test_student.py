import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    init_database()


def test_get_student_schedule():
    """
    Test student schedule retrieval.
    AC: [ARCH-5847-AC3] Students can view their adaptive study schedule on the Student Dashboard.
    """
    response = client.get("/api/v1/student/schedule?user_id=usr_alex_001")
    assert response.status_code == 200
    data = response.json()
    assert "blocks" in data
    assert len(data["blocks"]) >= 3
    block_topics = [b["topic"] for b in data["blocks"]]
    assert any("Dynamic Programming" in t for t in block_topics)


def test_toggle_study_block_completion():
    """
    Test toggle study block completion state and adherence calculation.
    AC: [ARCH-5847-AC3] Students can view their adaptive study schedule on the Student Dashboard.
    """
    response = client.post(
        "/api/v1/student/schedule/blocks/blk_001/toggle",
        json={"completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "blk_001"
    assert data["status"] == "Completed"
    assert "adherence_rate" in data


def test_get_student_progress():
    """
    Test student progress metrics and velocity.
    AC: [ARCH-5847-AC3] Students can view their adaptive study schedule on the Student Dashboard.
    """
    response = client.get("/api/v1/student/progress?user_id=usr_alex_001")
    assert response.status_code == 200
    data = response.json()
    assert data["weekly_hours_target"] == 20.0
    assert data["velocity_score"] > 0
