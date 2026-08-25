from app.db.session import SessionLocal
from app.models.question import Question

SAMPLES = [
    {
        "text": "She _____ to the store every Saturday.",
        "option_a": "go",
        "option_b": "goes",
        "option_c": "going",
        "option_d": "gone",
        "correct_option": "B",
        "difficulty": "A1",
    },
    {
        "text": "If it rains tomorrow, we _____ stay at home.",
        "option_a": "will",
        "option_b": "would",
        "option_c": "are",
        "option_d": "have",
        "correct_option": "A",
        "difficulty": "A2",
    },
    {
        "text": "The book _____ by millions of people last year.",
        "option_a": "reads",
        "option_b": "was read",
        "option_c": "is reading",
        "option_d": "has read",
        "correct_option": "B",
        "difficulty": "B1",
    },
    {
        "text": "I wish I _____ more time to finish the project.",
        "option_a": "have",
        "option_b": "had",
        "option_c": "will have",
        "option_d": "having",
        "correct_option": "B",
        "difficulty": "B2",
    },
    {
        "text": "Hardly _____ the door when the phone rang.",
        "option_a": "I had opened",
        "option_b": "had I opened",
        "option_c": "I opened",
        "option_d": "did I open",
        "correct_option": "B",
        "difficulty": "C1",
    },
]


def seed() -> None:
    db = SessionLocal()
    try:
        existing = db.query(Question).count()
        if existing > 0:
            print(f"Database already has {existing} questions. Skipping seed.")
            return

        for item in SAMPLES:
            db.add(Question(**item))
        db.commit()
        print(f"Inserted {len(SAMPLES)} sample questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
