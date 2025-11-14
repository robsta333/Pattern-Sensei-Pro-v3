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

# Multiple-choice distractor options
DISTRACTORS = [
    "Bullish continuation likely",
    "Bearish continuation likely",
    "Sideways consolidation likely",
    "Indecision — unclear direction",
    "Momentum weakening",
    "Trend exhaustion",
    "Reversal unlikely"
]


def generate_question(pattern_name):
    """
    Given a pattern, generate a multiple-choice prediction question.
    Returns:
        - question_text
        - choices (list)
        - correct_answer (string)
        - explanation (string)
    """

    correct_answer = PATTERN_BEHAVIOR[pattern_name]["expected"]
    explanation = PATTERN_BEHAVIOR[pattern_name]["explanation"]

    # Choose 3 fake answers that are not the correct one
    fake_answers = random.sample(
        [d for d in DISTRACTORS if d != correct_answer],
        3
    )

    # Insert the correct answer into the list randomly
    choices = fake_answers + [correct_answer]
    random.shuffle(choices)

    question_text = "Based on this pattern, what is the most likely market behavior?"

    return question_text, choices, correct_answer, explanation
