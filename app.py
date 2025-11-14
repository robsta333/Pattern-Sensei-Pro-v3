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
# HOME PAGE
# -----------------------------------------------------

if page == "Home":
    st.title("📈 Trading Education Game")
    st.write("Welcome to your interactive candlestick training app!")
    st.markdown("""
    This app now supports:
    - 🕹️ Pattern previews  
    - ❓ Prediction quizzes  
    - 🧠 Correct/incorrect feedback  
    - 🔄 Fully reset when switching patterns  
    """)
    st.info("Click *Training Game* to begin your practice.")


# -----------------------------------------------------
# TRAINING GAME PAGE — FULLY FIXED LOGIC
# -----------------------------------------------------

elif page == "Training Game":
    st.title("🕹️ Training Game — Pattern Prediction Quiz")
    st.write("Choose a pattern, generate a question, and test your prediction skills.")

    # -----------------------------------------------
    # PATTERN SELECTION
    # -----------------------------------------------
    pattern_choice = st.selectbox(
        "Choose a pattern:",
        ["Doji", "Hammer", "Shooting Star", "Bullish Engulfing", "Bearish Engulfing"],
        key="pattern_choice"
    )

    # -----------------------------------------------
    # SESSION STATE INITIALIZATION
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

    # -----------------------------------------------
    # RESET QUIZ IF PATTERN CHANGES
    # -----------------------------------------------
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
        xaxis_rangeslider_visible=False,
        xaxis_title="Candle Index",
        yaxis_title="Price"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------
    # QUIZ LOGIC
    # -----------------------------------------------
    st.subheader("❓ Prediction Question")

    # Generate new question
    if st.button("Generate Question"):
        q, choices, correct, expl = game_logic.generate_question(pattern_choice)
        st.session_state.quiz_state["generated"] = True
        st.session_state.quiz_state["question_text"] = q
        st.session_state.quiz_state["choices"] = choices
        st.session_state.quiz_state["correct_answer"] = correct
        st.session_state.quiz_state["explanation"] = expl
        st.session_state.quiz_state["user_answer"] = None

    # Display question
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

        # Show feedback
        if st.session_state.quiz_state["user_answer"] is not None:
            if st.session_state.quiz_state["user_answer"] == st.session_state.quiz_state["correct_answer"]:
                st.success("Correct! 🎉")
            else:
                st.error(
                    f"Incorrect. The correct answer is: **{st.session_state.quiz_state['correct_answer']}**"
                )

            st.info(f"📘 Explanation: {st.session_state.quiz_state['explanation']}")


# -----------------------------------------------------
# STATISTICS PAGE
# -----------------------------------------------------

elif page == "Statistics":
    st.title("📊 Statistics")
    st.write("Scoring and progress tracking will be added next.")
    st.info("Your accuracy, streaks, and pattern weaknesses will appear here soon!")
