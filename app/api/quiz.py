from fastapi import APIRouter, HTTPException
import uuid
from app.db.init_db import get_db_connection
from app.models.quiz import (
    QuizHistoryResponse,
    QuizHistoryItem,
    QuizGenerateRequest,
    QuizGenerateResponse,
    QuizQuestionItem,
    QuizSubmitRequest,
    QuizSubmitResponse,
    QuestionBreakdown
)

router = APIRouter(prefix="/quizzes", tags=["Diagnostic Quiz Center"])


@router.get("/history", response_model=QuizHistoryResponse)
def get_quiz_history(user_id: str = "usr_alex_001"):
    """
    Students can see past results in the Quiz Center.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            s.id, q.course_code, q.topic, s.score_percent, s.total_questions, s.submitted_at
        FROM quiz_submissions s
        JOIN quizzes q ON s.quiz_id = q.id
        WHERE s.user_id = ?
        ORDER BY s.submitted_at DESC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    history = [
        QuizHistoryItem(
            id=row["id"],
            course_code=row["course_code"],
            topic=row["topic"],
            score_percent=float(row["score_percent"]),
            total_questions=int(row["total_questions"]),
            date=str(row["submitted_at"])[:10]
        )
        for row in rows
    ]

    return QuizHistoryResponse(quizzes=history)


@router.post("/generate", response_model=QuizGenerateResponse, status_code=201)
def generate_quiz(payload: QuizGenerateRequest, user_id: str = "usr_alex_001"):
    """
    Students can generate a quiz in the Quiz Center.
    """
    quiz_id = f"quiz_{uuid.uuid4().hex[:8]}"
    count = max(1, min(payload.question_count, 10))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quizzes (id, user_id, course_code, topic, difficulty, question_count) VALUES (?, ?, ?, ?, ?, ?)",
        (quiz_id, user_id, payload.course_code.upper(), payload.topic, payload.difficulty, count)
    )

    questions_out = []
    # Seed dynamic questions for the requested topic
    sample_pool = [
        {
            "q": f"What is the foundational principle underlying {payload.topic}?",
            "a": "Modular decomposition and invariant validation",
            "b": "Brute-force iteration over memory states",
            "c": "Unchecked pointer arithmetic",
            "d": "Random state transitions",
            "correct": "A",
            "exp": f"The principle of {payload.topic} relies on formal modular decomposition."
        },
        {
            "q": f"How is performance optimization typically achieved in {payload.topic}?",
            "a": "Reducing asymptotic complexity and utilizing memoization",
            "b": "Increasing thread count indefinitely",
            "c": "Disabling compiler safety checks",
            "d": "Ignoring cache locality",
            "correct": "A",
            "exp": f"Performance in {payload.topic} focuses on minimizing complexity and caching."
        },
        {
            "q": f"Which diagnostic metric evaluates mastery in {payload.topic}?",
            "a": "Cyclomatic test coverage and problem-solving velocity",
            "b": "Source lines of comments",
            "c": "Hardware disk utilization",
            "d": "Elapsed idle time",
            "correct": "A",
            "exp": f"Mastery of {payload.topic} is measured via structured accuracy."
        }
    ]

    for idx in range(count):
        q_data = sample_pool[idx % len(sample_pool)]
        q_id = f"q_{uuid.uuid4().hex[:8]}"
        cursor.execute(
            """
            INSERT INTO quiz_questions
            (id, quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                q_id, quiz_id, q_data["q"], q_data["a"], q_data["b"],
                q_data["c"], q_data["d"], q_data["correct"], q_data["exp"]
            )
        )
        questions_out.append(
            QuizQuestionItem(
                id=q_id,
                question=q_data["q"],
                options=[
                    f"A: {q_data['a']}",
                    f"B: {q_data['b']}",
                    f"C: {q_data['c']}",
                    f"D: {q_data['d']}"
                ]
            )
        )

    conn.commit()
    conn.close()

    return QuizGenerateResponse(
        quiz_id=quiz_id,
        course_code=payload.course_code.upper(),
        topic=payload.topic,
        questions=questions_out
    )


@router.post("/{quiz_id}/submit", response_model=QuizSubmitResponse)
def submit_quiz(quiz_id: str, payload: QuizSubmitRequest, user_id: str = "usr_alex_001"):
    """
    Submit quiz answers and receive instant diagnostic score and explanations.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, question_text, correct_option, explanation FROM quiz_questions WHERE quiz_id = ?",
        (quiz_id,)
    )
    questions = cursor.fetchall()

    if not questions:
        conn.close()
        raise HTTPException(status_code=404, detail="Quiz not found or has no questions.")

    ans_map = {ans.question_id: ans.selected_option.upper().strip() for ans in payload.answers}
    correct_count = 0
    breakdown = []

    for q in questions:
        qid = q["id"]
        expected = q["correct_option"].upper().strip()
        user_choice = ans_map.get(qid, "")
        is_correct = (user_choice == expected) or (user_choice.startswith(expected))
        if is_correct:
            correct_count += 1
        breakdown.append(
            QuestionBreakdown(
                question_id=qid,
                correct=is_correct,
                explanation=q["explanation"]
            )
        )

    total_q = len(questions)
    score_pct = round((correct_count / total_q) * 100.0, 1) if total_q > 0 else 0.0
    feedback = (
        "Outstanding performance! Full mastery demonstrated."
        if score_pct >= 80.0 else
        "Good effort. Focus on reviewing the highlighted concepts."
    )

    sub_id = f"sub_{uuid.uuid4().hex[:8]}"
    cursor.execute(
        """
        INSERT INTO quiz_submissions
        (id, quiz_id, user_id, score_percent, correct_count, total_questions, diagnostic_feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (sub_id, quiz_id, user_id, score_pct, correct_count, total_q, feedback)
    )
    conn.commit()
    conn.close()

    return QuizSubmitResponse(
        quiz_id=quiz_id,
        score_percent=score_pct,
        correct_count=correct_count,
        total_questions=total_q,
        diagnostic_feedback=feedback,
        breakdown=breakdown
    )
