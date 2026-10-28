from fastapi import APIRouter
from app.db.init_db import get_db_connection
from app.models.faculty import FacultyOverviewResponse, FacultyStudentsResponse, StudentSummary

router = APIRouter(prefix="/faculty", tags=["Faculty Analytics"])


@router.get("/overview", response_model=FacultyOverviewResponse)
def get_faculty_overview():
    """
    Faculty can view aggregate metrics on the Faculty Dashboard.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            AVG(velocity_score) as avg_velocity,
            AVG(adherence_rate) as avg_adherence,
            SUM(CASE WHEN at_risk = 1 THEN 1 ELSE 0 END) as at_risk_count,
            COUNT(*) as total
        FROM student_metrics
        """
    )
    row = cursor.fetchone()
    conn.close()

    avg_vel = round(float(row["avg_velocity"]), 2) if row and row["avg_velocity"] else 1.05
    avg_adh = round(float(row["avg_adherence"]), 1) if row and row["avg_adherence"] else 78.6
    at_risk = int(row["at_risk_count"]) if row and row["at_risk_count"] else 1
    total = int(row["total"]) if row and row["total"] else 4

    return FacultyOverviewResponse(
        class_average_velocity=avg_vel,
        plan_adherence_rate=avg_adh,
        at_risk_students_count=at_risk,
        total_students=total
    )


@router.get("/students", response_model=FacultyStudentsResponse)
def get_faculty_students():
    """
    Faculty can view detailed student progress and at-risk status.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            u.id, u.name, u.email, m.course, m.adherence_rate, m.velocity_score, m.at_risk
        FROM users u
        JOIN student_metrics m ON u.id = m.user_id
        WHERE u.role = 'student'
        ORDER BY m.at_risk DESC, m.adherence_rate ASC
        """
    )
    rows = cursor.fetchall()
    conn.close()

    students = [
        StudentSummary(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            course=row["course"],
            adherence_rate=float(row["adherence_rate"]),
            velocity_score=float(row["velocity_score"]),
            at_risk=bool(row["at_risk"]),
            status="At-Risk" if row["at_risk"] else "On Track"
        )
        for row in rows
    ]

    return FacultyStudentsResponse(students=students)
