from fastapi import APIRouter, HTTPException
from app.db.init_db import get_db_connection
from app.models.schedule import (
    ScheduleResponse,
    StudyBlock,
    ToggleBlockRequest,
    ToggleBlockResponse,
    StudentProgressResponse
)

router = APIRouter(prefix="/student", tags=["Student Schedule & Progress"])


@router.get("/schedule", response_model=ScheduleResponse)
def get_student_schedule(user_id: str = "usr_alex_001"):
    """
    Students can view their adaptive study schedule on the Student Dashboard.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, course_code, topic, time_range, duration_minutes, cognitive_load, status, schedule_date
        FROM study_blocks
        WHERE user_id = ?
        ORDER BY id ASC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    blocks = [
        StudyBlock(
            id=row["id"],
            course_code=row["course_code"],
            topic=row["topic"],
            time_range=row["time_range"],
            duration_minutes=row["duration_minutes"],
            cognitive_load=row["cognitive_load"],
            status=row["status"]
        )
        for row in rows
    ]

    date_str = rows[0]["schedule_date"] if rows else "2026-07-23"
    return ScheduleResponse(date=date_str, blocks=blocks)


@router.post("/schedule/blocks/{block_id}/toggle", response_model=ToggleBlockResponse)
def toggle_study_block(block_id: str, payload: ToggleBlockRequest):
    """
    Toggle study block completion state and recalculate student adherence rate.
    """
    new_status = "Completed" if payload.completed else "Pending"
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM study_blocks WHERE id = ?", (block_id,))
    block = cursor.fetchone()
    if not block:
        conn.close()
        raise HTTPException(status_code=404, detail="Study block not found.")

    user_id = block["user_id"]
    cursor.execute("UPDATE study_blocks SET status = ? WHERE id = ?", (new_status, block_id))

    # Recalculate adherence
    query = """
        SELECT COUNT(*) as total, SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as done
        FROM study_blocks WHERE user_id = ?
    """
    cursor.execute(query, (user_id,))
    stats = cursor.fetchone()
    total = stats["total"] if stats and stats["total"] else 1
    done = stats["done"] if stats and stats["done"] else 0
    new_adherence = round((done / total) * 100.0, 1)

    cursor.execute(
        "UPDATE student_metrics SET adherence_rate = ? WHERE user_id = ?",
        (new_adherence, user_id)
    )
    conn.commit()
    conn.close()

    return ToggleBlockResponse(id=block_id, status=new_status, adherence_rate=new_adherence)


@router.get("/progress", response_model=StudentProgressResponse)
def get_student_progress(user_id: str = "usr_alex_001"):
    """
    Get student study metrics, velocity score, and weekly adherence.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT weekly_hours_target, hours_completed, adherence_rate, velocity_score
        FROM student_metrics WHERE user_id = ?
        """,
        (user_id,)
    )
    metric = cursor.fetchone()
    conn.close()

    if not metric:
        return StudentProgressResponse(
            weekly_hours_target=20.0,
            hours_completed=16.5,
            adherence_rate=82.5,
            velocity_score=1.15
        )

    return StudentProgressResponse(
        weekly_hours_target=metric["weekly_hours_target"],
        hours_completed=metric["hours_completed"],
        adherence_rate=metric["adherence_rate"],
        velocity_score=metric["velocity_score"]
    )
