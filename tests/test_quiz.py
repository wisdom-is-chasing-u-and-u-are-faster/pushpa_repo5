import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    init_database()


def test_get_quiz_history():
    """
    Test quiz history retrieval.
    AC: [ARCH-5847-AC6] Students can generate a quiz and see past results in the Quiz Center.
    """
    response = client.get("/api/v1/quizzes/history?user_id=usr_alex_001")
    assert response.status_code == 200
    data = response.json()
    assert "quizzes" in data
    assert len(data["quizzes"]) >= 2


def test_generate_and_submit_quiz():
    """
    Test generating a diagnostic quiz and submitting responses for instant diagnostic feedback.
    AC: [ARCH-5847-AC6] Students can generate a quiz and see past results in the Quiz Center.
    """
    # 1. Generate Quiz
    gen_res = client.post(
        "/api/v1/quizzes/generate?user_id=usr_alex_001",
        json={
            "course_code": "CS301",
            "topic": "Graph Algorithms",
            "question_count": 2,
            "difficulty": "Medium"
        }
    )
    assert gen_res.status_code == 201
    quiz_data = gen_res.json()
    quiz_id = quiz_data["quiz_id"]
    assert len(quiz_data["questions"]) == 2

    # 2. Submit Answers
    answers = [
        {"question_id": q["id"], "selected_option": "A"}
        for q in quiz_data["questions"]
    ]
    sub_res = client.post(
        f"/api/v1/quizzes/{quiz_id}/submit?user_id=usr_alex_001",
        json={"answers": answers}
    )
    assert sub_res.status_code == 200
    result = sub_res.json()
    assert result["quiz_id"] == quiz_id
    assert "score_percent" in result
    assert "diagnostic_feedback" in result
    assert len(result["breakdown"]) == 2
