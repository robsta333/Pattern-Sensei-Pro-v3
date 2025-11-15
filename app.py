import streamlit as st
import plotly.graph_objects as go
import pandas as pd

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
    ["Home", "Training Game", "Statistics"]
)

# -----------------------------------------------------
# INITIALIZE GLOBAL SCORING STATE
# -----------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = {
        "correct": 0,
        "incorrect": 0,
        "current_streak": 0,
        "best_streak": 0
    }


# -----------------------------------------------------
# HOME PAGE
# -----------------------------------------------------

if page == "Home":
    st.title("📈 Trading Education Game")
    st.write("Welcome to your interactive candlestick training app!")
    st.markdown("""
    This version includes:
    - 🕹️ Pattern previews  
    - ❓ Prediction quizzes  
    - 🧠 Correct/incorrect feedback  
    - 📊 Persistent scoring (correct / incorrect / streaks / accuracy)  
    """)
    st.info("Begin training by selecting **Training Game** in the sidebar.")


# -----------------------------------------------------
# TRAINING GAME PAGE — WITH SCORING
# -----------------------------------------------------

elif page == "Training Game":
    st.title("🕹️ Training Game — Pattern Prediction Quiz")
    st.write("Choose a pattern, generate a question, test your skills, and build your score.")

    # -----------------------------------------------
    # PATTERN SELECTION
    # -----------------------------------------------
    pattern_choice = st.selectbox(
        "Choose a pattern:",
        ["Doji", "Hammer", "Shooting Star", "Bullish Engulfing", "Bearish Engulfing"],
        key="pattern_choice"
    )

    # -----------------------------------------------
    # SESSION STATE FOR QUIZ LOGIC
    # -----------------------------------------------
    if "current_pattern" not in st.session_state:
        st.session_state.current_pattern = pattern_choice

    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = {
            "generated": False,
            "question_text": None,
            "choices": None,
            "correct_answer": None,
            "explanation": None,
            "user_answer": None
        }

    # Reset quiz when pattern changes
    if st.session_state.current_pattern != pattern_choice:
        st.session_state.current_pattern = pattern_choice
        st.session_state.quiz_state = {
            "generated": False,
            "question_text": None,
            "choices": None,
            "correct_answer": None,
            "explanation": None,
            "user_answer": None
        }

    # -----------------------------------------------
    # GENERATE PATTERN AND DISPLAY CHART
    # -----------------------------------------------
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

    # -----------------------------------------------
    # QUIZ QUESTION GENERATION
    # -----------------------------------------------
    st.subheader("❓ Prediction Question")

    if st.button("Generate Question"):
        q, choices, correct, expl = game_logic.generate_question(pattern_choice)
        st.session_state.quiz_state = {
            "generated": True,
            "question_text": q,
            "choices": choices,
            "correct_answer": correct,
            "explanation": expl,
            "user_answer": None
        }

    # Display question when ready
    if st.session_state.quiz_state["generated"]:
        st.write(st.session_state.quiz_state["question_text"])

        user_answer = st.radio(
            "Your answer:",
            st.session_state.quiz_state["choices"],
            key="answer_radio"
        )

        # Submit logic
        if st.button("Submit Answer"):
            st.session_state.quiz_state["user_answer"] = user_answer

            # ----------------------------
            # SCORING UPDATE
            # ----------------------------
            if user_answer == st.session_state.quiz_state["correct_answer"]:
                st.success("Correct! 🎉")
                st.session_state.score["correct"] += 1
                st.session_state.score["current_streak"] += 1

                # Update best streak
                if st.session_state.score["current_streak"] > st.session_state.score["best_streak"]:
                    st.session_state.score["best_streak"] = st.session_state.score["current_streak"]

            else:
                st.error(
                    f"Incorrect. The correct answer is: **{st.session_state.quiz_state['correct_answer']}**"
                )
                st.session_state.score["incorrect"] += 1
                st.session_state.score["current_streak"] = 0

            st.info(f"📘 Explanation: {st.session_state.quiz_state['explanation']}")

    # -----------------------------------------------
    # DISPLAY CURRENT STATS INLINE
    # -----------------------------------------------
    st.markdown("---")
    st.subheader("📊 Live Statistics")

    correct = st.session_state.score["correct"]
    incorrect = st.session_state.score["incorrect"]
    total = correct + incorrect
    accuracy = (correct / total * 100) if total > 0 else 0

    st.write(f"**Correct:** {correct}")
    st.write(f"**Incorrect:** {incorrect}")
    st.write(f"**Accuracy:** {accuracy:.1f}%")
    st.write(f"**Current streak:** {st.session_state.score['current_streak']}")
    st.write(f"**Best streak:** {st.session_state.score['best_streak']}")


# -----------------------------------------------------
# STATISTICS PAGE
# -----------------------------------------------------

elif page == "Statistics":
    st.title("📊 Statistics")

    correct = st.session_state.score["correct"]
    incorrect = st.session_state.score["incorrect"]
    total = correct + incorrect
    accuracy = (correct / total * 100) if total > 0 else 0

    st.subheader("Your Performance")
    st.write(f"**Total questions:** {total}")
    st.write(f"**Correct answers:** {correct}")
    st.write(f"**Incorrect answers:** {incorrect}")
    st.write(f"**Accuracy:** {accuracy:.1f}%")
    st.write(f"**Best streak:** {st.session_state.score['best_streak']}")

    st.info("As you play more questions, your statistics will update automatically.")
