from pydantic import BaseModel
from typing import List


class StudentSummary(BaseModel):
    id: str
    name: str
    email: str
    course: str
    adherence_rate: float
    velocity_score: float
    at_risk: bool
    status: str


class FacultyOverviewResponse(BaseModel):
    class_average_velocity: float
    plan_adherence_rate: float
    at_risk_students_count: int
    total_students: int


class FacultyStudentsResponse(BaseModel):
    students: List[StudentSummary]
