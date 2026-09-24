"""
Insert sample questions for the English placement exam.

Usage (from backend folder):
    $env:PYTHONPATH = "."     # Windows PowerShell
    export PYTHONPATH=.       # Linux / macOS

    python scripts/seed_sample_questions.py
    python scripts/seed_sample_questions.py --force   # delete old samples and re-insert
"""

import sys

from app.db.session import SessionLocal
from app.models.question import Question

# ~60 accurate MCQs across CEFR levels (balanced for a 20-question exam)
SAMPLES = [
    # ========== A1 (basic grammar / everyday English) ==========
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
    {
        "text": "This is _____ apple.",
        "option_a": "a",
        "option_b": "an",
        "option_c": "the",
        "option_d": "— (no article)",
        "correct_option": "B",
        "difficulty": "A1",
    },
    {
        "text": "They _____ at home yesterday.",
        "option_a": "is",
        "option_b": "are",
        "option_c": "was",
        "option_d": "were",
        "correct_option": "D",
        "difficulty": "A1",
    },
    {
        "text": "My brother _____ in London.",
        "option_a": "live",
        "option_b": "lives",
        "option_c": "living",
        "option_d": "lived",
        "correct_option": "B",
        "difficulty": "A1",
    },
    {
        "text": "_____ is your name?",
        "option_a": "Who",
        "option_b": "What",
        "option_c": "Where",
        "option_d": "When",
        "correct_option": "B",
        "difficulty": "A1",
    },
    {
        "text": "I can _____ English a little.",
        "option_a": "speak",
        "option_b": "to speak",
        "option_c": "speaking",
        "option_d": "spoke",
        "correct_option": "A",
        "difficulty": "A1",
    },
    {
        "text": "The cat is _____ the chair.",
        "option_a": "in",
        "option_b": "on",
        "option_c": "at",
        "option_d": "to",
        "correct_option": "B",
        "difficulty": "A1",
    },

    # ========== A2 (simple past, comparatives, basic connectors) ==========
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
    {
        "text": "I went to the cinema _____ I was tired.",
        "option_a": "because",
        "option_b": "so",
        "option_c": "but",
        "option_d": "although",
        "correct_option": "C",
        "difficulty": "A2",
    },
    {
        "text": "He has _____ finished his homework.",
        "option_a": "yet",
        "option_b": "already",
        "option_c": "still",
        "option_d": "ever",
        "correct_option": "B",
        "difficulty": "A2",
    },
    {
        "text": "Could you _____ me the salt, please?",
        "option_a": "pass",
        "option_b": "to pass",
        "option_c": "passing",
        "option_d": "passed",
        "correct_option": "A",
        "difficulty": "A2",
    },
    {
        "text": "This bag is _____ expensive for me.",
        "option_a": "too",
        "option_b": "enough",
        "option_c": "very much",
        "option_d": "so much",
        "correct_option": "A",
        "difficulty": "A2",
    },
    {
        "text": "I _____ to the park last Sunday.",
        "option_a": "go",
        "option_b": "goes",
        "option_c": "went",
        "option_d": "gone",
        "correct_option": "C",
        "difficulty": "A2",
    },
    {
        "text": "She doesn't like coffee, and _____ do I.",
        "option_a": "so",
        "option_b": "neither",
        "option_c": "either",
        "option_d": "too",
        "correct_option": "B",
        "difficulty": "A2",
    },

    # ========== B1 (present perfect, conditionals, passive basics) ==========
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
    {
        "text": "She has worked here _____ 2019.",
        "option_a": "for",
        "option_b": "since",
        "option_c": "during",
        "option_d": "from",
        "correct_option": "B",
        "difficulty": "B1",
    },
    {
        "text": "You _____ wear a helmet when you ride a bike.",
        "option_a": "should",
        "option_b": "would",
        "option_c": "might to",
        "option_d": "can to",
        "correct_option": "A",
        "difficulty": "B1",
    },
    {
        "text": "The meeting was cancelled _____ the bad weather.",
        "option_a": "because",
        "option_b": "because of",
        "option_c": "although",
        "option_d": "despite of",
        "correct_option": "B",
        "difficulty": "B1",
    },
    {
        "text": "I'm looking forward to _____ you again.",
        "option_a": "see",
        "option_b": "seeing",
        "option_c": "saw",
        "option_d": "seen",
        "correct_option": "B",
        "difficulty": "B1",
    },
    {
        "text": "By next year, she _____ her degree.",
        "option_a": "finishes",
        "option_b": "will finish",
        "option_c": "will have finished",
        "option_d": "has finished",
        "correct_option": "C",
        "difficulty": "B1",
    },
    {
        "text": "He asked me where I _____.",
        "option_a": "live",
        "option_b": "lived",
        "option_c": "am living",
        "option_d": "do live",
        "correct_option": "B",
        "difficulty": "B1",
    },

    # ========== B2 (inversion-light, conditionals, phrasal verbs, relative clauses) ==========
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
    {
        "text": "_____ the weather, the event will go ahead as planned.",
        "option_a": "Although",
        "option_b": "Despite",
        "option_c": "However",
        "option_d": "Whereas",
        "correct_option": "B",
        "difficulty": "B2",
    },
    {
        "text": "The report, _____ was published yesterday, caused a lot of debate.",
        "option_a": "who",
        "option_b": "which",
        "option_c": "what",
        "option_d": "whose",
        "correct_option": "B",
        "difficulty": "B2",
    },
    {
        "text": "If she _____ harder, she would have passed the exam.",
        "option_a": "studied",
        "option_b": "had studied",
        "option_c": "has studied",
        "option_d": "would study",
        "correct_option": "B",
        "difficulty": "B2",
    },
    {
        "text": "I'll pick you _____ at the station at 6.",
        "option_a": "on",
        "option_b": "up",
        "option_c": "out",
        "option_d": "off",
        "correct_option": "B",
        "difficulty": "B2",
    },
    {
        "text": "It's high time we _____ a decision.",
        "option_a": "make",
        "option_b": "made",
        "option_c": "making",
        "option_d": "to make",
        "correct_option": "B",
        "difficulty": "B2",
    },
    {
        "text": "Neither the manager nor the employees _____ informed.",
        "option_a": "was",
        "option_b": "were",
        "option_c": "is",
        "option_d": "be",
        "correct_option": "B",
        "difficulty": "B2",
    },

    # ========== C1 (advanced inversion, subjunctive, nuanced grammar) ==========
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
    {
        "text": "She spoke as if she _____ the answer all along.",
        "option_a": "knows",
        "option_b": "knew",
        "option_c": "has known",
        "option_d": "had known",
        "correct_option": "D",
        "difficulty": "C1",
    },
    {
        "text": "The proposal was accepted _____ some minor reservations.",
        "option_a": "in spite",
        "option_b": "despite",
        "option_c": "although",
        "option_d": "however",
        "correct_option": "B",
        "difficulty": "C1",
    },
    {
        "text": "Only after the results were published _____ the full impact.",
        "option_a": "we understood",
        "option_b": "did we understand",
        "option_c": "we did understand",
        "option_d": "understood we",
        "correct_option": "B",
        "difficulty": "C1",
    },
    {
        "text": "I'd rather you _____ that in front of the client.",
        "option_a": "don't say",
        "option_b": "didn't say",
        "option_c": "haven't said",
        "option_d": "not say",
        "correct_option": "B",
        "difficulty": "C1",
    },
    {
        "text": "The more he explained, _____ confused I became.",
        "option_a": "the more",
        "option_b": "more",
        "option_c": "the most",
        "option_d": "most",
        "correct_option": "A",
        "difficulty": "C1",
    },
    {
        "text": "Such _____ the demand that the product sold out in hours.",
        "option_a": "was",
        "option_b": "were",
        "option_c": "is",
        "option_d": "are",
        "correct_option": "A",
        "difficulty": "C1",
    },

    # ========== C2 (near-native structures and precise vocabulary) ==========
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
        "text": "The committee recommended that the policy _____ immediately.",
        "option_a": "is changed",
        "option_b": "be changed",
        "option_c": "was changed",
        "option_d": "changed",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "Little _____ that the decision would have such consequences.",
        "option_a": "he knew",
        "option_b": "did he know",
        "option_c": "he did know",
        "option_d": "knew he",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "The findings were at _____ with earlier research.",
        "option_a": "odds",
        "option_b": "odds ends",
        "option_c": "odd",
        "option_d": "odds with",
        "correct_option": "A",
        "difficulty": "C2",
    },
    {
        "text": "Were it not for her support, the project _____ failed.",
        "option_a": "would",
        "option_b": "would have",
        "option_c": "had",
        "option_d": "will have",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "He is widely regarded as _____ authority on the subject.",
        "option_a": "a",
        "option_b": "an",
        "option_c": "the",
        "option_d": "— (no article)",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "The plan fell _____ due to a lack of funding.",
        "option_a": "out",
        "option_b": "through",
        "option_c": "apart",
        "option_d": "off",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "In no way _____ responsible for the delay.",
        "option_a": "the company is",
        "option_b": "is the company",
        "option_c": "the company was",
        "option_d": "was the company being",
        "correct_option": "B",
        "difficulty": "C2",
    },
    {
        "text": "Her argument was _____ convincing that few disagreed.",
        "option_a": "so",
        "option_b": "such",
        "option_c": "too",
        "option_d": "enough",
        "correct_option": "A",
        "difficulty": "C2",
    },
]


def seed(force: bool = False) -> None:
    db = SessionLocal()
    try:
        existing = db.query(Question).count()

        if existing > 0 and not force:
            print(f"Database already has {existing} questions. Skipping seed.")
            print("Use --force to delete existing questions and insert the new set.")
            return

        if force and existing > 0:
            deleted = db.query(Question).delete()
            db.commit()
            print(f"Deleted {deleted} existing questions.")

        for item in SAMPLES:
            db.add(Question(**item))
        db.commit()
        print(f"Inserted {len(SAMPLES)} sample questions.")
        print("Levels: A1–C2, ~10 questions each.")
    finally:
        db.close()


if __name__ == "__main__":
    force = "--force" in sys.argv
    seed(force=force)
