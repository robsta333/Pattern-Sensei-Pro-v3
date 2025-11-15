import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Import modules
import patterns
import game_logic

# -----------------------------------------------------
# BASIC APP SETUP
# -----------------------------------------------------

st.set_page_config(
    page_title="Trading Education Game",
    page_icon="📈",
    layout="centered"
)

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.title("📘 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Home", "Training Game", "Predict the Next Candle", "Statistics"]
)

# -----------------------------------------------------
# GLOBAL SCORING STATE (SHARED BY BOTH MODES)
# -----------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = {
        "correct": 0,
        "incorrect": 0,
        "current_streak": 0,
        "best_streak": 0
    }

# Utility function to compute accuracy
def compute_accuracy():
    correct = st.session_state.score["correct"]
    incorrect = st.session_state.score["incorrect"]
    total = correct + incorrect
    if total == 0:
        return 0.0
    return correct / total * 100.0


# =====================================================
# HOME PAGE
# =====================================================

if page == "Home":
    st.title("📈 Trading Education Game")
    st.write("Welcome to your interactive candlestick training app!")
    st.markdown("""
    This app currently includes:
    - 🕹️ **Training Game** — Learn what classic candlestick patterns *mean*  
    - 🔮 **Predict the Next Candle** — Practice guessing what comes next in a sequence  
    - 📊 **Statistics** — Track your accuracy, streaks, and progress  
    """)
    st.info("Use the sidebar to switch between modes.")


# =====================================================
# TRAINING GAME — PATTERN MEANING QUIZ
# =====================================================

elif page == "Training Game":
    st.title("🕹️ Training Game — Pattern Meaning Quiz")
    st.write("Choose a pattern, generate a question, test your understanding, and build your score.")

    # ---------------- Pattern selection ----------------
    pattern_choice = st.selectbox(
        "Choose a pattern:",
        ["Doji", "Hammer", "Shooting Star", "Bullish Engulfing", "Bearish Engulfing"],
        key="pattern_choice"
    )

    # ---------------- Session state for this mode ----------------
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

    # ---------------- Generate and plot the pattern ----------------
    df = patterns.get_pattern(pattern_choice)

    st.subheader(f"Pattern Preview: {pattern_choice}")

    fig = go.Figure(data=[go.Candlestick(
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        increasing_line_color="green",
        decreasing_line_color="red",
        increasing_fillcolor="green",
        decreasing_fillcolor="red",
        increasing_line_width=2,
        decreasing_line_width=2
    )])

    fig.update_layout(
        height=400,
        width=600,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Quiz generation ----------------
    st.subheader("❓ Prediction Question (Pattern Meaning)")

    if st.button("Generate Question", key="generate_pattern_question"):
        q, choices, correct, expl = game_logic.generate_question(pattern_choice)
        st.session_state.pattern_quiz_state = {
            "generated": True,
            "question_text": q,
            "choices": choices,
            "correct_answer": correct,
            "explanation": expl,
            "user_answer": None
        }

    # Display question when ready
    if st.session_state.pattern_quiz_state["generated"]:
        st.write(st.session_state.pattern_quiz_state["question_text"])

        user_answer = st.radio(
            "Your answer:",
            st.session_state.pattern_quiz_state["choices"],
            key="pattern_answer_radio"
        )

        if st.button("Submit Answer", key="submit_pattern_answer"):
            st.session_state.pattern_quiz_state["user_answer"] = user_answer

            if user_answer == st.session_state.pattern_quiz_state["correct_answer"]:
                st.success("Correct! 🎉")
                st.session_state.score["correct"] += 1
                st.session_state.score["current_streak"] += 1
                if st.session_state.score["current_streak"] > st.session_state.score["best_streak"]:
                    st.session_state.score["best_streak"] = st.session_state.score["current_streak"]
            else:
                st.error(
                    f"Incorrect. The correct answer is: **{st.session_state.pattern_quiz_state['correct_answer']}**"
                )
                st.session_state.score["incorrect"] += 1
                st.session_state.score["current_streak"] = 0

            st.info(f"📘 Explanation: {st.session_state.pattern_quiz_state['explanation']}")

    # ---------------- Inline stats ----------------
    st.markdown("---")
    st.subheader("📊 Live Statistics (All Modes)")
    accuracy = compute_accuracy()
    st.write(f"**Correct:** {st.session_state.score['correct']}")
    st.write(f"**Incorrect:** {st.session_state.score['incorrect']}")
    st.write(f"**Accuracy:** {accuracy:.1f}%")
    st.write(f"**Current streak:** {st.session_state.score['current_streak']}")
    st.write(f"**Best streak:** {st.session_state.score['best_streak']}")


# =====================================================
# PREDICT THE NEXT CANDLE — NEW MODE
# =====================================================

elif page == "Predict the Next Candle":
    st.title("🔮 Predict the Next Candle")
    st.write("Look at the recent sequence of candles and guess what the next candle will be.")

    # ---------------- Session state for this mode ----------------
    if "next_mode_state" not in st.session_state:
        st.session_state.next_mode_state = {
            "sequence_df": None,
            "question_active": False,
            "user_answer": None,
            "correct_label": None,
            "revealed": False
        }

    # Helper: generate a random price sequence
    def generate_price_sequence(num_candles=10):
        prices = [100.0]
        for _ in range(num_candles):
            delta = np.random.normal(0, 0.6)
            prices.append(prices[-1] + delta)

        opens, highs, lows, closes = [], [], [], []
        for i in range(num_candles):
            o = prices[i]
            c = prices[i + 1]
            high = max(o, c) + np.random.uniform(0.1, 0.5)
            low = min(o, c) - np.random.uniform(0.1, 0.5)
            opens.append(o)
            highs.append(high)
            lows.append(low)
            closes.append(c)

        return pd.DataFrame({
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes
        })

    # Helper: classify a candle
    def classify_candle(o, c, h, l):
        body = abs(c - o)
        range_ = h - l
        if range_ == 0:
            return "Doji / indecision"
        body_ratio = body / range_
        if body_ratio < 0.2:
            return "Doji / indecision"
        elif c > o:
            return "Bullish candle"
        else:
            return "Bearish candle"

    # ---------------- Generate new sequence button ----------------
    if st.button("Generate New Sequence"):
        df_seq = generate_price_sequence(num_candles=10)
        st.session_state.next_mode_state["sequence_df"] = df_seq
        st.session_state.next_mode_state["question_active"] = True
        st.session_state.next_mode_state["user_answer"] = None
        st.session_state.next_mode_state["revealed"] = False

        # Last candle is the "hidden" next candle
        last = df_seq.iloc[-1]
        st.session_state.next_mode_state["correct_label"] = classify_candle(
            last["open"], last["close"], last["high"], last["low"]
        )

    # If we have an active sequence/question
    if st.session_state.next_mode_state["question_active"] and st.session_state.next_mode_state["sequence_df"] is not None:
        df_seq = st.session_state.next_mode_state["sequence_df"]

        # Show all candles except the last one
        visible_df = df_seq.iloc[:-1]

        st.subheader("Price Action (last candle hidden)")
        fig2 = go.Figure(data=[go.Candlestick(
            open=visible_df["open"],
            high=visible_df["high"],
            low=visible_df["low"],
            close=visible_df["close"],
            increasing_line_color="green",
            decreasing_line_color="red",
            increasing_fillcolor="green",
            decreasing_fillcolor="red",
            increasing_line_width=2,
            decreasing_line_width=2
        )])

        fig2.update_layout(
            height=400,
            width=600,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("❓ What is the most likely next candle?")

        choices = ["Bullish candle", "Bearish candle", "Doji / indecision"]

        user_answer_next = st.radio(
            "Your answer:",
            choices,
            key="next_mode_radio"
        )

        if st.button("Submit Prediction"):
            st.session_state.next_mode_state["user_answer"] = user_answer_next
            st.session_state.next_mode_state["revealed"] = True

            correct_label = st.session_state.next_mode_state["correct_label"]

            if user_answer_next == correct_label:
                st.success("Correct! 🎉")
                st.session_state.score["correct"] += 1
                st.session_state.score["current_streak"] += 1
                if st.session_state.score["current_streak"] > st.session_state.score["best_streak"]:
                    st.session_state.score["best_streak"] = st.session_state.score["current_streak"]
            else:
                st.error(f"Incorrect. The correct answer was: **{correct_label}**")
                st.session_state.score["incorrect"] += 1
                st.session_state.score["current_streak"] = 0

        # Reveal the hidden next candle and full sequence
        if st.session_state.next_mode_state["revealed"]:
            st.markdown("---")
            st.subheader("🔍 Revealed: Full Sequence with Next Candle")

            full_df = st.session_state.next_mode_state["sequence_df"]

            fig3 = go.Figure(data=[go.Candlestick(
                open=full_df["open"],
                high=full_df["high"],
                low=full_df["low"],
                close=full_df["close"],
                increasing_line_color="green",
                decreasing_line_color="red",
                increasing_fillcolor="green",
                decreasing_fillcolor="red",
                increasing_line_width=2,
                decreasing_line_width=2
            )])

            fig3.update_layout(
                height=400,
                width=600,
                margin=dict(l=40, r=40, t=40, b=40),
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig3, use_container_width=True)

            st.caption("The final candle was the one you were trying to predict.")

    st.markdown("---")
    st.subheader("📊 Live Statistics (All Modes)")
    accuracy = compute_accuracy()
    st.write(f"**Correct:** {st.session_state.score['correct']}")
    st.write(f"**Incorrect:** {st.session_state.score['incorrect']}")
    st.write(f"**Accuracy:** {accuracy:.1f}%")
    st.write(f"**Current streak:** {st.session_state.score['current_streak']}")
    st.write(f"**Best streak:** {st.session_state.score['best_streak']}")


# =====================================================
# STATISTICS PAGE
# =====================================================

elif page == "Statistics":
    st.title("📊 Statistics")

    correct = st.session_state.score["correct"]
    incorrect = st.session_state.score["incorrect"]
    total = correct + incorrect
    accuracy = compute_accuracy()

    st.subheader("Overall Performance")
    st.write(f"**Total questions (all modes):** {total}")
    st.write(f"**Correct answers:** {correct}")
    st.write(f"**Incorrect answers:** {incorrect}")
    st.write(f"**Accuracy:** {accuracy:.1f}%")
    st.write(f"**Best streak:** {st.session_state.score['best_streak']}")

    st.info("Both the Pattern Meaning Game and Predict the Next Candle mode contribute to these stats.")
