

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.exam import Exam
from app.models.question import Question
from app.schemas.result import SubmitAnswersRequest, ResultResponse
from app.core.security import get_current_user  # JWT dependency (placeholder)

router = APIRouter(
    prefix="/results",
    tags=["Results"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/submit", response_model=ResultResponse)
def submit_exam_answers(
    payload: SubmitAnswersRequest,
    db: Session = Depends(get_db),
):
    exam = db.query(Exam).filter(Exam.id == payload.exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    if exam.score is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exam already submitted"
        )

    question_ids = list(payload.answers.keys())
    if not question_ids:
        raise HTTPException(status_code=400, detail="No answers submitted")

    questions = (
        db.query(Question)
        .filter(Question.id.in_(question_ids))
        .all()
    )

    if len(questions) != len(question_ids):
        raise HTTPException(
            status_code=400,
            detail="Invalid question IDs detected"
        )

    score = 0
    for q in questions:
        submitted = payload.answers.get(q.id)
        if submitted and submitted.upper() == q.correct_option.upper():
            score += 1

    total = len(questions)

    if score <= 4:
        cefr = "A1"
    elif score <= 7:
        cefr = "A2"
    elif score <= 10:
        cefr = "B1"
    elif score <= 14:
        cefr = "B2"
    elif score <= 17:
        cefr = "C1"
    else:
        cefr = "C2"

    exam.score = score
    exam.cefr_level = cefr

    db.commit()
    db.refresh(exam)

    return ResultResponse(
        score=score,
        total=total,
        cefr_level=cefr
    )
