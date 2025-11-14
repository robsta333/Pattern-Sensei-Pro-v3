import random

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

# Cleaner distractors
DISTRACTORS = [
    "Bullish continuation likely",
    "Bearish continuation likely",
    "Sideways consolidation likely",
    "Momentum weakening",
    "Trend exhaustion",
    "Reversal unlikely"
]

def generate_question(pattern_name):
    """Generate a multiple-choice question for the selected pattern."""
    correct_answer = PATTERN_BEHAVIOR[pattern_name]["expected"]
    explanation = PATTERN_BEHAVIOR[pattern_name]["explanation"]

    # Avoid distractors that repeat key words from the correct answer
    keywords = ["indecision", "reversal", "pause"]
    filtered = []
    for d in DISTRACTORS:
        if not any(kw in d.lower() for kw in keywords):
            filtered.append(d)

    while len(filtered) < 3:
        filtered.append("No clear signal")

    fake_answers = random.sample(filtered, 3)
    choices = fake_answers + [correct_answer]
    random.shuffle(choices)

    question_text = "Based on this pattern, what is the most likely market behavior?"

    return question_text, choices, correct_answer, explanation
