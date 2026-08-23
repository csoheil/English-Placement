from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.exam import Exam
from app.models.user import User
from app.api.deps import get_current_user
from app.services.pagination import paginate

router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get("/")
def get_exam_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return paginated exam history for the authenticated user.
    """
    query = (
        db.query(Exam)
        .filter(Exam.user_id == current_user.id)
        .order_by(Exam.id.desc())
    )

    exams, total = paginate(query, page, page_size)

    # Convert ORM objects to plain dicts so FastAPI can serialize them
    data = [
        {
            "id": exam.id,
            "score": exam.score,
            "cefr_level": exam.cefr_level,
        }
        for exam in exams
    ]

    return {
        "data": data,
        "meta": {
            "page": page,
            "page_size": page_size,
            "total": total,
        },
    }
