from pydantic import BaseModel
from typing import List


class StudyBlock(BaseModel):
    id: str
    course_code: str
    topic: str
    time_range: str
    duration_minutes: int
    cognitive_load: str
    status: str


class ScheduleResponse(BaseModel):
    date: str
    blocks: List[StudyBlock]


class ToggleBlockRequest(BaseModel):
    completed: bool


class ToggleBlockResponse(BaseModel):
    id: str
    status: str
    adherence_rate: float


class StudentProgressResponse(BaseModel):
    weekly_hours_target: float
    hours_completed: float
    adherence_rate: float
    velocity_score: float
