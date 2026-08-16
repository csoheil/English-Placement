from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.exam import Exam
from app.models.question import Question
from app.models.result import Result
from app.models.user import User
from app.schemas.result import SubmitAnswersRequest, ResultResponse
from app.services.scoring import calculate_score, map_score_to_cefr

router = APIRouter(
    prefix="/results",
    tags=["Results"],
)


@router.post("/submit", response_model=ResultResponse)
def submit_exam_answers(
    payload: SubmitAnswersRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit answers for an exam, score them and store the result.
    """
    # Load the exam and make sure it belongs to the current user
    exam = (
        db.query(Exam)
        .filter(Exam.id == payload.exam_id, Exam.user_id == current_user.id)
        .first()
    )
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    if exam.score is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exam already submitted",
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
            detail="Invalid question IDs detected",
        )

    # Score the answers
    score = calculate_score(questions, payload.answers)
    total = len(questions)
    cefr = map_score_to_cefr(score)

    # Update the exam record
    exam.score = score
    exam.cefr_level = cefr

    # Also create a Result row (used by progress / history endpoints)
    result = Result(
        user_id=current_user.id,
        exam_id=exam.id,
        score=score,
        total=total,
        cefr_level=cefr,
    )
    db.add(result)

    db.commit()
    db.refresh(exam)

    return ResultResponse(
        score=score,
        total=total,
        cefr_level=cefr,
    )
