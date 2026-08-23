from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.result import Result
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/cefr-distribution")
def cefr_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """
    Return CEFR level distribution across all submitted exams.
    Admin-only endpoint.
    """
    rows = (
        db.query(Result.cefr_level, func.count(Result.id))
        .group_by(Result.cefr_level)
        .all()
    )

    return {level: count for level, count in rows}
