import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    init_database()


def test_list_syllabi():
    """
    Test listing syllabi.
    AC: [ARCH-5847-AC5] Users can upload a syllabus via the Syllabus Management screen.
    """
    response = client.get("/api/v1/syllabi")
    assert response.status_code == 200
    data = response.json()
    assert "syllabi" in data
    assert len(data["syllabi"]) >= 3


def test_upload_syllabus_success():
    """
    Test uploading a syllabus and topic extraction.
    AC: [ARCH-5847-AC5] Users can upload a syllabus via the Syllabus Management screen.
    """
    payload = {
        "course_code": "CS401",
        "course_title": "Advanced Operating Systems",
        "term": "Fall 2026",
        "syllabus_text": "1. Kernel Architecture & IPC\n2. Virtual Memory Management\n3. File System Internals"
    }
    response = client.post("/api/v1/syllabi/upload", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["course_code"] == "CS401"
    assert data["status"] == "PROCESSED"
    assert len(data["extracted_topics"]) == 3
