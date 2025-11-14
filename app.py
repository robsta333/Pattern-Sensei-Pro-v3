import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Import the pattern generator module
import patterns

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
    st.write("Welcome! This is the base of your interactive trading education platform.")
    st.markdown("""
    In the next steps, you will:
    - 🕹️ Train on candlestick patterns  
    - 🔍 Learn reversal & continuation signals  
    - 📊 Improve your recognition accuracy  
    """)
    st.info("Your app is running correctly. Training visuals now available under the Training Game tab.")

# -----------------------------------------------------
# TRAINING GAME PAGE — PATTERN PREVIEW
# -----------------------------------------------------

elif page == "Training Game":
    st.title("🕹️ Training Game")
    st.write("Select a candlestick pattern to preview it. More game mechanics coming soon!")

    # Dropdown for selecting the pattern
    pattern_choice = st.selectbox(
        "Choose a pattern:",
        ["Doji", "Hammer", "Shooting Star", "Bullish Engulfing", "Bearish Engulfing"]
    )

    # Generate data
    df = patterns.get_pattern(pattern_choice)

    st.subheader(f"Pattern Preview: {pattern_choice}")

    # Plotly candlestick chart
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

    st.success("Pattern generator working. Game logic is next!")

# -----------------------------------------------------
# STATISTICS PAGE
# -----------------------------------------------------

elif page == "Statistics":
    st.title("📊 Statistics")
    st.write("Your training performance will appear here later.")
