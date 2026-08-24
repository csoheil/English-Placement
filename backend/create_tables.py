"""
Create all database tables defined by the SQLAlchemy models.
Run once before starting the application:

    python create_tables.py
"""

from app.db.session import engine
from app.models.base import Base

# Import every model so that Base.metadata knows about them
from app.models.user import User  # noqa: F401
from app.models.question import Question  # noqa: F401
from app.models.exam import Exam  # noqa: F401
from app.models.result import Result  # noqa: F401


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")


if __name__ == "__main__":
    create_tables()
