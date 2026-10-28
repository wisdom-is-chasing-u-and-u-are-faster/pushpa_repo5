from pydantic import BaseModel
from typing import List


class SyllabusItem(BaseModel):
    id: str
    course_code: str
    course_title: str
    term: str
    topics_count: int
    status: str
    uploaded_at: str


class SyllabusListResponse(BaseModel):
    syllabi: List[SyllabusItem]


class SyllabusUploadRequest(BaseModel):
    course_code: str
    course_title: str
    term: str
    syllabus_text: str


class SyllabusUploadResponse(BaseModel):
    id: str
    course_code: str
    status: str
    extracted_topics: List[str]
