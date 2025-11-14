import random

# -----------------------------------------------------
# GAME LOGIC MODULE
# -----------------------------------------------------
# This module defines:
# - Expected behavior for each pattern
# - Multiple-choice answer generator
# - Explanations for correct answer
# -----------------------------------------------------

# Ground-truth behavior for the patterns
# These are simplified educational definitions
PATTERN_BEHAVIOR = {
    "Doji": {
        "expected": "Indecision — potential reversal or pause",
        "explanation": "A Doji signals market uncertainty. It often appears before a reversal but is not a guarantee on its own."
    },
    "Hammer": {
        "expected": "Bullish reversal likely",
        "explanation": "A Hammer forms after a decline and shows buyers stepping in strongly, rejecting lower prices."
    },
    "Shooting Star": {
        "expected": "Bearish reversal likely",
        "explanation": "A Shooting Star appears after a rise and signals exhaustion — buyers pushed price up but were overwhelmed."
    },
    "Bullish Engulfing": {
        "expected": "Bullish reversal likely",
        "explanation": "A Bullish Engulfing candle swallows the prior bearish candle, indicating strong buying pressure."
    },
    "Bearish Engulfing": {
        "expected": "Bearish reversal likely",
        "explanation": "A Bearish Engulfing candle overwhelms the prior bullish candle, signaling aggressive selling."
    }
}

# Multiple-choice distractor options (cleaned to avoid duplicates)
DISTRACTORS = [
    "Bullish continuation likely",
    "Bearish continuation likely",
    "Sideways consolidation likely",
    "Momentum weakening",
    "Trend exhaustion",
    "Reversal unlikely"
]

def generate_question(pattern_name):
    """
    Generate a multiple-choice question for the selected pattern.
    Ensures no distractor contains overlapping wording with the correct answer.
    """
    correct_answer = PATTERN_BEHAVIOR[pattern_name]["expected"]
    explanation = PATTERN_BEHAVIOR[pattern_name]["explanation"]

    # Filter out any distractor containing key words from the correct answer
    keywords = ["indecision", "reversal", "pause"]
    filtered = []

    for d in DISTRACTORS:
        if not any(kw.lower() in d.lower() for kw in keywords):
            filtered.append(d)

    # Ensure we have enough distractors (fallback if needed)
    while len(filtered) < 3:
        filtered.append("No clear signal")

    # Choose 3 fake answers
    fake_answers = random.sample(filtered, 3)

    # Insert the correct one and shuffle
    choices = fake_answers + [correct_answer]
    random.shuffle(choices)

    question_text = "Based on this pattern, what is the most likely market behavior?"

    return question_text, choices, correct_answer, explanation
