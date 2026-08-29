
from app.db.session import SessionLocal
from app.models.question import Question

# Around 25 questions across CEFR levels (enough for a 20-question exam)
SAMPLES = [
    # --- A1 ---
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
        "text": "I _____ a student.",
        "option_a": "is",
        "option_b": "are",
        "option_c": "am",
        "option_d": "be",
        "correct_option": "C",
        "difficulty": "A1",
    },
    {
        "text": "There _____ two books on the table.",
        "option_a": "is",
        "option_b": "are",
        "option_c": "be",
        "option_d": "was",
        "correct_option": "B",
        "difficulty": "A1",
    },
    {
        "text": "_____ you like coffee?",
        "option_a": "Does",
        "option_b": "Do",
        "option_c": "Is",
        "option_d": "Are",
        "correct_option": "B",
        "difficulty": "A1",
    },
    # --- A2 ---
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
        "text": "I have lived here _____ five years.",
        "option_a": "since",
        "option_b": "for",
        "option_c": "during",
        "option_d": "from",
        "correct_option": "B",
        "difficulty": "A2",
    },
    {
        "text": "She is _____ than her sister.",
        "option_a": "tall",
        "option_b": "taller",
        "option_c": "tallest",
        "option_d": "more tall",
        "correct_option": "B",
        "difficulty": "A2",
    },
    {
        "text": "They _____ TV when I called.",
        "option_a": "watched",
        "option_b": "were watching",
        "option_c": "watch",
        "option_d": "are watching",
        "correct_option": "B",
        "difficulty": "A2",
    },
    # --- B1 ---
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
        "text": "If I _____ more time, I would travel more.",
        "option_a": "have",
        "option_b": "had",
        "option_c": "will have",
        "option_d": "having",
        "correct_option": "B",
        "difficulty": "B1",
    },
    {
        "text": "He suggested that we _____ early.",
        "option_a": "leave",
        "option_b": "left",
        "option_c": "leaving",
        "option_d": "to leave",
        "correct_option": "A",
        "difficulty": "B1",
    },
    {
        "text": "I've never _____ such a beautiful place.",
        "option_a": "see",
        "option_b": "saw",
        "option_c": "seen",
        "option_d": "seeing",
        "correct_option": "C",
        "difficulty": "B1",
    },
    # --- B2 ---
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
        "text": "By the time we arrived, the film _____.",
        "option_a": "started",
        "option_b": "has started",
        "option_c": "had started",
        "option_d": "was starting",
        "correct_option": "C",
        "difficulty": "B2",
    },
    {
        "text": "She is used to _____ early every morning.",
        "option_a": "get up",
        "option_b": "getting up",
        "option_c": "got up",
        "option_d": "gets up",
        "correct_option": "B",
        "difficulty": "B2",
    },
    {
        "text": "Not only _____ late, but he also forgot the documents.",
        "option_a": "he was",
        "option_b": "was he",
        "option_c": "he is",
        "option_d": "is he",
        "correct_option": "B",
        "difficulty": "B2",
    },
    # --- C1 ---
    {
        "text": "Hardly _____ the door when the phone rang.",
        "option_a": "I had opened",
        "option_b": "had I opened",
        "option_c": "I opened",
        "option_d": "did I open",
        "correct_option": "B",
        "difficulty": "C1",
    },
    {
        "text": "It is essential that every student _____ the form.",
        "option_a": "completes",
        "option_b": "complete",
        "option_c": "completed",
        "option_d": "completing",
        "correct_option": "B",
        "difficulty": "C1",
    },
    {
        "text": "No sooner _____ the announcement than people started to leave.",
        "option_a": "had been made",
        "option_b": "was made",
        "option_c": "has been made",
        "option_d": "is made",
        "correct_option": "A",
        "difficulty": "C1",
    },
    {
        "text": "Had I known about the traffic, I _____ earlier.",
        "option_a": "left",
        "option_b": "would leave",
        "option_c": "would have left",
        "option_d": "had left",
        "correct_option": "C",
        "difficulty": "C1",
    },
    # --- C2 / mixed advanced ---
    {
        "text": "The proposal was rejected on the _____ that it was too expensive.",
        "option_a": "base",
        "option_b": "basis",
        "option_c": "basic",
        "option_d": "basement",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "Scarcely _____ the results when the media started calling.",
        "option_a": "we had announced",
        "option_b": "had we announced",
        "option_c": "we announced",
        "option_d": "did we announce",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "She spoke as if she _____ the answer all along.",
        "option_a": "knows",
        "option_b": "knew",
        "option_c": "has known",
        "option_d": "had known",
        "correct_option": "D",
        "difficulty": "C2",
    },
    {
        "text": "The committee recommended that the policy _____ immediately.",
        "option_a": "is changed",
        "option_b": "be changed",
        "option_c": "was changed",
        "option_d": "changed",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "_____ the weather, the event will go ahead as planned.",
        "option_a": "Although",
        "option_b": "Despite",
        "option_c": "However",
        "option_d": "Whereas",
        "correct_option": "B",
        "difficulty": "B2",
    },
]


def seed() -> None:
    db = SessionLocal()
    try:
        existing = db.query(Question).count()
        if existing > 0:
            print(f"Database already has {existing} questions. Skipping seed.")
            print("Tip: delete english.db and run create_tables.py + this script again if you want a fresh set.")
            return

        for item in SAMPLES:
            db.add(Question(**item))
        db.commit()
        print(f"Inserted {len(SAMPLES)} sample questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
