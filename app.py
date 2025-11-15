import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Import your local modules
import patterns
import game_logic

# -----------------------------------------------------
# STREAMLIT CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Trading Education Game",
    page_icon="📈",
    layout="centered"
)

# -----------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------

st.sidebar.title("📘 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Home", "Training Game", "Predict the Next Candle", "Statistics"]
)

# -----------------------------------------------------
# GLOBAL SCORING STATE
# -----------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = {
        "correct": 0,
        "incorrect": 0,
        "current_streak": 0,
        "best_streak": 0
    }

def compute_accuracy():
    c = st.session_state.score["correct"]
    i = st.session_state.score["incorrect"]
    t = c + i
    return (c / t * 100.0) if t > 0 else 0.0


# -----------------------------------------------------
# HOME PAGE
# -----------------------------------------------------

if page == "Home":
    st.title("📈 Trading Education Game")
    st.write("Welcome to your interactive candlestick training platform.")

    st.markdown("""
    ### Available Modes:
    **🕹️ Training Game**  
    Learn what classic candlestick patterns *mean*.

    **🔮 Predict the Next Candle**  
    Practice forecasting the next candle from real sequences.

    **📊 Statistics**  
    Track your accuracy, streaks, and progress.
    """)

    st.info("Use the sidebar to choose a mode.")


# =====================================================
# TRAINING GAME — CANDLE PATTERN MEANING QUIZ
# =====================================================

elif page == "Training Game":
    st.title("🕹️ Training Game — Pattern Meaning Quiz")

    pattern_choice = st.selectbox(
        "Choose a pattern:",
        ["Doji", "Hammer", "Shooting Star", "Bullish Engulfing", "Bearish Engulfing"],
        key="pattern_choice"
    )

    # Session state for this mode
    if "current_pattern" not in st.session_state:
        st.session_state.current_pattern = pattern_choice

    if "pattern_quiz_state" not in st.session_state:
        st.session_state.pattern_quiz_state = {
            "generated": False,
            "question_text": None,
            "choices": None,
            "correct_answer": None,
            "explanation": None,
            "user_answer": None
        }

    # Reset quiz if pattern changes
    if st.session_state.current_pattern != pattern_choice:
        st.session_state.current_pattern = pattern_choice
        st.session_state.pattern_quiz_state = {
            "generated": False,
            "question_text": None,
            "choices": None,
            "correct_answer": None,
            "explanation": None,
            "user_answer": None
        }

    # Plot pattern candles
    df = patterns.get_pattern(pattern_choice)

    st.subheader(f"Pattern Preview: {pattern_choice}")
    fig = go.Figure(data=[go.Candlestick(
        open=df["open"], high=df["high"], low=df["low"], close=df["close"],
        increasing_line_color="green", decreasing_line_color="red",
        increasing_fillcolor="green", decreasing_fillcolor="red"
    )])
    fig.update_layout(height=400, width=600, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("❓ Prediction Question (Pattern Meaning)")

    if st.button("Generate Question", key="generate_pattern_q"):
        q, choices, correct, expl = game_logic.generate_question(pattern_choice)
        st.session_state.pattern_quiz_state = {
            "generated": True,
            "question_text": q,
            "choices": choices,
            "correct_answer": correct,
            "explanation": expl,
            "user_answer": None
        }

    if st.session_state.pattern_quiz_state["generated"]:
        st.write(st.session_state.pattern_quiz_state["question_text"])

        user_answer = st.radio(
            "Your answer:",
            st.session_state.pattern_quiz_state["choices"],
            key="pattern_radio"
        )

        if st.button("Submit Answer", key="submit_pattern_q"):
            st.session_state.pattern_quiz_state["user_answer"] = user_answer

            if user_answer == st.session_state.pattern_quiz_state["correct_answer"]:
                st.success("Correct! 🎉")
                st.session_state.score["correct"] += 1
                st.session_state.score["current_streak"] += 1
                if st.session_state.score["current_streak"] > st.session_state.score["best_streak"]:
                    st.session_state.score["best_streak"] = st.session_state.score["current_streak"]
            else:
                st.error(
                    f"Incorrect. Correct answer: **{st.session_state.pattern_quiz_state['correct_answer']}**"
                )
                st.session_state.score["incorrect"] += 1
                st.session_state.score["current_streak"] = 0

            st.info(f"📘 Explanation: {st.session_state.pattern_quiz_state['explanation']}")

    # Inline stats
    st.markdown("---")
    st.subheader("📊 Live Stats")
    st.write(f"Correct: {st.session_state.score['correct']}")
    st.write(f"Incorrect: {st.session_state.score['incorrect']}")
    st.write(f"Accuracy: {compute_accuracy():.1f}%")
    st.write(f"Current streak: {st.session_state.score['current_streak']}")
    st.write(f"Best streak: {st.session_state.score['best_streak']}")


# =====================================================
# PREDICT THE NEXT CANDLE — NEW MODE
# =====================================================

elif page == "Predict the Next Candle":
    st.title("🔮 Predict the Next Candle")

    # -------------------------------------------------
    # State for this mode
    # -------------------------------------------------
    if "next_mode" not in st.session_state:
        st.session_state.next_mode = {
            "sequence_df": None,
            "hidden_label": None,
            "user_answer": None,
            "revealed": False
        }

    # -------------------------------------------------
    # Helpers: Candle classification & explanations
    # -------------------------------------------------

    def classify_candle(o, c, h, l):
        body = abs(c - o)
        rng = h - l
        if rng == 0:
            return "Doji / indecision"
        if body / rng < 0.2:
            return "Doji / indecision"
        return "Bullish candle" if c > o else "Bearish candle"

    def explain_candle(o, c, h, l):
        body = abs(c - o)
        rng = h - l
        if rng == 0 or body / rng < 0.2:
            return "Tiny body relative to range → indecision, market unsure."
        if c > o:
            return "Closed strongly above open → bullish control."
        return "Closed strongly below open → bearish control."

    def explain_sequence(df):
        closes = df["close"].values
        msg = ""

        # Trend direction
        if closes[-1] > closes[-3]:
            msg += "Higher closes recently → bullish pressure. "
        elif closes[-1] < closes[-3]:
            msg += "Lower closes recently → bearish pressure. "
        else:
            msg += "Flat closes → no clear trend. "

        # Wick behavior
        lows = df["low"].values
        highs = df["high"].values
        opens = df["open"].values
        last_low_wicks = [o - l for o, l in zip(opens[-3:], lows[-3:])]
        last_high_wicks = [h - c for h, c in zip(highs[-3:], closes[-3:])]

        if sum(last_low_wicks) > sum(last_high_wicks):
            msg += "Longer lower wicks → buying support. "
        elif sum(last_high_wicks) > sum(last_low_wicks):
            msg += "Longer upper wicks → selling pressure. "
        else:
            msg += "Balanced wicks → indecision. "

        return msg.strip()

    # -------------------------------------------------
    # Generate random price sequence
    # -------------------------------------------------

    def generate_sequence(n=10):
        prices = [100]
        for _ in range(n):
            prices.append(prices[-1] + np.random.normal(0, 0.6))

        opens, highs, lows, closes = [], [], [], []
        for i in range(n):
            o = prices[i]
            c = prices[i+1]
            high = max(o, c) + np.random.uniform(0.1, 0.5)
            low = min(o, c) - np.random.uniform(0.1, 0.5)
            opens.append(o); highs.append(high); lows.append(low); closes.append(c)

        return pd.DataFrame({
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes
        })

    # -------------------------------------------------
    # Generate new sequence
    # -------------------------------------------------

    if st.button("Generate New Sequence"):
        df = generate_sequence()
        st.session_state.next_mode["sequence_df"] = df
        last = df.iloc[-1]
        st.session_state.next_mode["hidden_label"] = classify_candle(
            last["open"], last["close"], last["high"], last["low"]
        )
        st.session_state.next_mode["user_answer"] = None
        st.session_state.next_mode["revealed"] = False

    # -------------------------------------------------
    # Display hidden sequence
    # -------------------------------------------------

    if st.session_state.next_mode["sequence_df"] is not None:
        df = st.session_state.next_mode["sequence_df"]
        visible = df.iloc[:-1]

        st.subheader("Price Action (Last Candle Hidden)")

        fig = go.Figure(data=[go.Candlestick(
            open=visible["open"], high=visible["high"],
            low=visible["low"], close=visible["close"],
            increasing_line_color="green", decreasing_line_color="red"
        )])
        fig.update_layout(height=400, width=600, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("❓ What is the most likely next candle?")

        choices = ["Bullish candle", "Bearish candle", "Doji / indecision"]

        user_answer = st.radio("Choose:", choices, key="next_prediction_radio")

        if st.button("Submit Prediction"):
            st.session_state.next_mode["user_answer"] = user_answer
            st.session_state.next_mode["revealed"] = True

            correct = st.session_state.next_mode["hidden_label"]

            if user_answer == correct:
                st.success("Correct prediction! 🎉")
                st.session_state.score["correct"] += 1
                st.session_state.score["current_streak"] += 1
                if st.session_state.score["current_streak"] > st.session_state.score["best_streak"]:
                    st.session_state.score["best_streak"] = st.session_state.score["current_streak"]
            else:
                st.error(f"Incorrect. The correct answer was: **{correct}**")
                st.session_state.score["incorrect"] += 1
                st.session_state.score["current_streak"] = 0

        # -------------------------------------------------
        # Reveal full sequence + explanation
        # -------------------------------------------------
        if st.session_state.next_mode["revealed"]:
            st.markdown("---")
            st.subheader("🔍 Revealed: Full Sequence")

            # Plot full sequence
            fig2 = go.Figure(data=[go.Candlestick(
                open=df["open"], high=df["high"], low=df["low"], close=df["close"],
                increasing_line_color="green", decreasing_line_color="red"
            )])
            fig2.update_layout(height=400, width=600, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig2, use_container_width=True)

            # Explanation blocks
            st.markdown("### 🧠 Why This Candle Formed")

            seq_expl = explain_sequence(df.iloc[:-1])
            candle_expl = explain_candle(
                df.iloc[-1]["open"], df.iloc[-1]["close"],
                df.iloc[-1]["high"], df.iloc[-1]["low"]
            )

            st.write(f"**Sequence context:** {seq_expl}")
            st.write(f"**Candle behavior:** {candle_expl}")

    # Inline stats
    st.markdown("---")
    st.subheader("📊 Live Stats")
    st.write(f"Correct: {st.session_state.score['correct']}")
    st.write(f"Incorrect: {st.session_state.score['incorrect']}")
    st.write(f"Accuracy: {compute_accuracy():.1f}%")
    st.write(f"Current streak: {st.session_state.score['current_streak']}")
    st.write(f"Best streak: {st.session_state.score['best_streak']}")


# =====================================================
# STATISTICS PAGE
# =====================================================

elif page == "Statistics":
    st.title("📊 Statistics")

    accuracy = compute_accuracy()
    st.subheader("Overall Performance")

    st.write(f"**Correct answers:** {st.session_state.score['correct']}")
    st.write(f"**Incorrect answers:** {st.session_state.score['incorrect']}")
    st.write(f"**Accuracy:** {accuracy:.1f}%")
    st.write(f"**Best streak:** {st.session_state.score['best_streak']}")

    st.info("Both modes contribute to your statistics.")
