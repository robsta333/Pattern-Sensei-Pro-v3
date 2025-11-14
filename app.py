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
    st.write("Welcome! This is the start of your interactive trading education platform.")
    st.markdown("""
    The platform now supports:
    - 🕹️ Pattern previews  
    - ❓ Prediction quizzes  
    - 🧠 Immediate feedback  
    """)
    st.info("Go to the Training Game tab to start practicing candlestick patterns!")


# -----------------------------------------------------
# TRAINING GAME PAGE — FULL QUIZ LOGIC WITH SESSION STATE
# -----------------------------------------------------

elif page == "Training Game":
    st.title("🕹️ Training Game — Candlestick Pattern Quiz")

    st.write("Select a pattern, generate a quiz question, and test your prediction skills!")

    # Pattern selection dropdown
    pattern_choice = st.selectbox(
        "Choose a pattern:",
        ["Doji", "Hammer", "Shooting Star", "Bullish Engulfing", "Bearish Engulfing"],
        key="pattern_choice"
    )

    # Generate pattern candles
    df = patterns.get_pattern(pattern_choice)

    st.subheader(f"Pattern Preview: {pattern_choice}")

    # Build and display candlestick chart
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

    st.subheader("❓ Prediction Question")

    # -------------------------------------------
    # Initialize session state variables
    # -------------------------------------------
    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = {
            "question_generated": False,
            "question_text": None,
            "choices": None,
            "correct_answer": None,
            "explanation": None,
            "user_answer": None
        }

    # -------------------------------------------
    # Generate a new question
    # -------------------------------------------
    if st.button("Generate Question"):
        q_text, choices, correct, explanation = game_logic.generate_question(pattern_choice)

        st.session_state.quiz_state["question_generated"] = True
        st.session_state.quiz_state["question_text"] = q_text
        st.session_state.quiz_state["choices"] = choices
        st.session_state.quiz_state["correct_answer"] = correct
        st.session_state.quiz_state["explanation"] = explanation
        st.session_state.quiz_state["user_answer"] = None

    # -------------------------------------------
    # Display question + answer radio button
    # -------------------------------------------
    if st.session_state.quiz_state["question_generated"]:
        st.write(st.session_state.quiz_state["question_text"])

        user_answer = st.radio(
            "Your answer:",
            st.session_state.quiz_state["choices"],
            key="user_answer_radio"
        )

        # Submit button
        if st.button("Submit Answer"):
            st.session_state.quiz_state["user_answer"] = user_answer

        # -------------------------------------------
        # Show feedback
        # -------------------------------------------
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
    st.write("Your accuracy, streaks, and performance summaries will appear here in a future update.")
    st.info("This section will grow as we build the full game system.")
