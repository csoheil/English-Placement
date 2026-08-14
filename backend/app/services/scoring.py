from typing import Dict, List, Any


def calculate_score(questions: List[Any], answers: Dict[int, str]) -> int:
    """
    Count how many answers match the correct option.

    questions: list of objects that have .id and .correct_option
    answers:   dict mapping question_id -> selected option (A/B/C/D)
    """
    score = 0
    for q in questions:
        submitted = answers.get(q.id)
        if submitted is None:
            continue
        if submitted.upper() == q.correct_option.upper():
            score += 1
    return score


def map_score_to_cefr(score: int) -> str:
    """
    Map a raw score (out of 20) to a CEFR level.
    Thresholds are intentionally simple for a placement test.
    """
    if score <= 4:
        return "A1"
    if score <= 7:
        return "A2"
    if score <= 10:
        return "B1"
    if score <= 14:
        return "B2"
    if score <= 17:
        return "C1"
    return "C2"


# Keep the old name as an alias so existing call-sites do not break
calculate_cefr_level = map_score_to_cefr
