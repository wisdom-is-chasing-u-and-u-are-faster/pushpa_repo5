from fastapi import APIRouter, HTTPException
import uuid
import datetime
from app.db.init_db import get_db_connection
from app.models.syllabus import (
    SyllabusListResponse,
    SyllabusItem,
    SyllabusUploadRequest,
    SyllabusUploadResponse
)

router = APIRouter(prefix="/syllabi", tags=["Syllabus Management"])


@router.get("", response_model=SyllabusListResponse)
def list_syllabi():
    """
    List all uploaded and processed syllabi.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            s.id, s.course_code, s.course_title, s.term, s.status, s.uploaded_at,
            COUNT(t.id) as topics_count
        FROM syllabi s
        LEFT JOIN syllabus_topics t ON s.id = t.syllabus_id
        GROUP BY s.id
        ORDER BY s.uploaded_at DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()

    syllabi = [
        SyllabusItem(
            id=row["id"],
            course_code=row["course_code"],
            course_title=row["course_title"],
            term=row["term"],
            topics_count=row["topics_count"],
            status=row["status"],
            uploaded_at=str(row["uploaded_at"])
        )
        for row in rows
    ]

    return SyllabusListResponse(syllabi=syllabi)


@router.post("/upload", response_model=SyllabusUploadResponse, status_code=201)
def upload_syllabus(payload: SyllabusUploadRequest):
    """
    Users can upload a syllabus via the Syllabus Management screen.
    Parses course details and extracts structured topics.
    """
    syllabus_id = f"syl_{uuid.uuid4().hex[:8]}"
    uploaded_at = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Simple heuristic topic extraction from lines
    lines = [line.strip() for line in payload.syllabus_text.splitlines() if line.strip()]
    extracted = []
    for line in lines:
        if line.startswith(("-", "*", "•", "1.", "2.", "3.", "4.", "5.", "Week", "Module", "Topic")):
            clean_topic = line.lstrip("-*• 0123456789.:").strip()
            if clean_topic:
                extracted.append(clean_topic)

    if not extracted:
        extracted = [
            f"{payload.course_code} Core Foundations",
            f"{payload.course_code} Intermediate Applications",
            f"{payload.course_code} Advanced Synthesis & Projects"
        ]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO syllabi (id, course_code, course_title, term, status, uploaded_at) VALUES (?, ?, ?, ?, ?, ?)",
        (syllabus_id, payload.course_code.upper(), payload.course_title, payload.term, "PROCESSED", uploaded_at)
    )

    for idx, top in enumerate(extracted, start=1):
        top_id = f"top_{uuid.uuid4().hex[:8]}"
        cursor.execute(
            "INSERT INTO syllabus_topics (id, syllabus_id, topic_name, order_index) VALUES (?, ?, ?, ?)",
            (top_id, syllabus_id, top, idx)
        )

    conn.commit()
    conn.close()

    return SyllabusUploadResponse(
        id=syllabus_id,
        course_code=payload.course_code.upper(),
        status="PROCESSED",
        extracted_topics=extracted
    )


@router.delete("/{syllabus_id}")
def delete_syllabus(syllabus_id: str):
    """Deletes a syllabus by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM syllabi WHERE id = ?", (syllabus_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    if not deleted:
        raise HTTPException(status_code=404, detail="Syllabus not found.")

    return {"status": "deleted", "id": syllabus_id}
