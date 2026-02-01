# backend/app/schemas/result.py

from pydantic import BaseModel
from typing import Dict


class SubmitAnswersRequest(BaseModel):
    exam_id: int
    answers: Dict[int, str]  # question_id -> selected option (A/B/C/D)


class ResultResponse(BaseModel):
    score: int
    total: int
    cefr_level: str
