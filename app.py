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
    st.write("Welcome! This is the beginning of your interactive trading education platform.")
    st.markdown("""
    You can now:
    - 🕹️ Preview candlestick patterns  
    - ❓ Answer prediction questions  
    - 🧠 Test your intuition  
    """)
    st.info("Go to the Training Game tab to play the first version of the game!")

# -----------------------------------------------------
# TRAINING GAME PAGE — QUIZ MODE
# -----------------------------------------------------

elif page == "Training Game":
    st.title("🕹️ Training Game")

    st.write("Select a pattern to preview it and answer the prediction question.")

    # Choose a pattern
    pattern_choice = st.selectbox(
        "Choose a pattern:",
        ["Doji", "Hammer", "Shooting Star", "Bullish Engulfing", "Bearish Engulfing"]
    )

    # Generate the candlestick pattern
    df = patterns.get_pattern(pattern_choice)

    st.subheader(f"Pattern Preview: {pattern_choice}")

    # Plot the candlestick chart
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

    # -----------------------------------------------------
    # QUIZ LOGIC
    # -----------------------------------------------------

    st.subheader("❓ Prediction Question")

    # Get the question and answer choices
    question_text, choices, correct_answer, explanation = game_logic.generate_question(pattern_choice)

    st.write(question_text)

    # Radio buttons for user selection
    user_answer = st.radio("Your answer:", choices)

    # Submit button
    if st.button("Submit Answer"):
        if user_answer == correct_answer:
            st.success("Correct! 🎉")
        else:
            st.error(f"Incorrect. The correct answer is: **{correct_answer}**")

        st.info(f"📘 Explanation: {explanation}")

# -----------------------------------------------------
# STATISTICS PAGE
# -----------------------------------------------------

elif page == "Statistics":
    st.title("📊 Statistics")
    st.write("Your performance stats will appear here in a later version.")
