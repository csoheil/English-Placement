
from pydantic import BaseModel
from typing import List, Dict

class ExamStartResponse(BaseModel):
    exam_id: int
    questions: List[dict]

class AnswerSubmission(BaseModel):
    answers: Dict[int, str]  # question_id -> selected option

class ExamResultResponse(BaseModel):
    score: int
    total: int
    cefr_level: str
