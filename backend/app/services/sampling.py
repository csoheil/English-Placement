
from sqlalchemy.orm import Session
from app.models.question import Question
import random

def get_random_questions(db: Session, limit: int = 20):
    max_id = db.query(Question.id).order_by(Question.id.desc()).first()[0]

    random_ids = set()
    while len(random_ids) < limit:
        random_ids.add(random.randint(1, max_id))

    questions = (
        db.query(Question)
        .filter(Question.id.in_(random_ids))
        .all()
    )

    return questions
