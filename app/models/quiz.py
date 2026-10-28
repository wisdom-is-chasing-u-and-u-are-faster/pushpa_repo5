from pydantic import BaseModel
from typing import List


class QuizQuestionItem(BaseModel):
    id: str
    question: str
    options: List[str]


class QuizHistoryItem(BaseModel):
    id: str
    course_code: str
    topic: str
    score_percent: float
    total_questions: int
    date: str


class QuizHistoryResponse(BaseModel):
    quizzes: List[QuizHistoryItem]


class QuizGenerateRequest(BaseModel):
    course_code: str
    topic: str
    question_count: int = 5
    difficulty: str = "Medium"


class QuizGenerateResponse(BaseModel):
    quiz_id: str
    course_code: str
    topic: str
    questions: List[QuizQuestionItem]


class AnswerSubmission(BaseModel):
    question_id: str
    selected_option: str


class QuizSubmitRequest(BaseModel):
    answers: List[AnswerSubmission]


class QuestionBreakdown(BaseModel):
    question_id: str
    correct: bool
    explanation: str


class QuizSubmitResponse(BaseModel):
    quiz_id: str
    score_percent: float
    correct_count: int
    total_questions: int
    diagnostic_feedback: str
    breakdown: List[QuestionBreakdown]
