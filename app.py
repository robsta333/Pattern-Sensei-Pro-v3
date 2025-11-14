import streamlit as st

# -----------------------------
# BASIC APP SETUP (STEP 1)
# -----------------------------

st.set_page_config(
    page_title="Trading Education Game",
    page_icon="📈",
    layout="centered"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📘 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Home", "Training Game (Coming Soon)", "Statistics (Coming Soon)"]
)

# -----------------------------
# HOME PAGE
# -----------------------------
if page == "Home":
    st.title("📈 Trading Education Game")
    st.write("Welcome! This is the starting point for building your training game.")
    st.write("In the next steps, we will add:")
    st.markdown("""
    - 🕹️ Interactive candlestick training game  
    - 🔍 Pattern recognition  
    - 📊 A scoring and statistics system  
    - 📈 Live or simulated chart segments  
    """)
    st.info("App is running correctly. Use this as your stable base.")

# -----------------------------
# TRAINING GAME PAGE (placeholder)
# -----------------------------
elif page == "Training Game (Coming Soon)":
    st.title("🕹️ Training Game")
    st.write("The game engine will be added in the next step.")
    st.write("Get ready for pattern quizzes and chart predictions!")

# -----------------------------
# STATISTICS PAGE (placeholder)
# -----------------------------
elif page == "Statistics (Coming Soon)":
    st.title("📊 Statistics")
    st.write("Your training stats will appear here once the game is live.")
    st.write("Accuracy, streaks, weak patterns, and more!")

import numpy as np
import pandas as pd

# -----------------------------------------------------
# Pattern Generator Module
# -----------------------------------------------------
# This generates clean candle data for training visuals.
# Each pattern returns a pandas DataFrame with OHLC data.
# -----------------------------------------------------

def generate_doji():
    open_price = 100
    close_price = open_price + np.random.uniform(-0.2, 0.2)
    high = open_price + np.random.uniform(0.5, 1.5)
    low = open_price - np.random.uniform(0.5, 1.5)
    return _create_df(open_price, high, low, close_price)


def generate_hammer():
    open_price = 100
    close_price = open_price + np.random.uniform(0.5, 1.0)  # close slightly above open
    low = open_price - np.random.uniform(2.0, 3.0)          # long lower shadow
    high = close_price + np.random.uniform(0.2, 0.5)
    return _create_df(open_price, high, low, close_price)


def generate_shooting_star():
    open_price = 100
    close_price = open_price - np.random.uniform(0.5, 1.0)  # bearish subtle close
    high = open_price + np.random.uniform(2.0, 3.0)         # long upper shadow
    low = close_price - np.random.uniform(0.2, 0.5)
    return _create_df(open_price, high, low, close_price)


def generate_bullish_engulfing():
    # candle 1: bearish
    o1 = 100
    c1 = o1 - np.random.uniform(1.0, 2.0)
    h1 = max(o1, c1) + np.random.uniform(0.2, 0.5)
    l1 = min(o1, c1) - np.random.uniform(0.2, 0.5)

    # candle 2: bullish engulfing
    o2 = c1 - np.random.uniform(0.5, 1.0)
    c2 = o1 + np.random.uniform(1.0, 2.0)
    h2 = max(o2, c2) + np.random.uniform(0.2, 0.5)
    l2 = min(o2, c2) - np.random.uniform(0.2, 0.5)

    data = [
        [o1, h1, l1, c1],
        [o2, h2, l2, c2]
    ]
    return _df_multi(data)


def generate_bearish_engulfing():
    # candle 1: bullish
    o1 = 100
    c1 = o1 + np.random.uniform(1.0, 2.0)
    h1 = max(o1, c1) + np.random.uniform(0.2, 0.5)
    l1 = min(o1, c1) - np.random.uniform(0.2, 0.5)

    # candle 2: bearish engulfing
    o2 = c1 + np.random.uniform(0.5, 1.0)
    c2 = o1 - np.random.uniform(1.0, 2.0)
    h2 = max(o2, c2) + np.random.uniform(0.2, 0.5)
    l2 = min(o2, c2) - np.random.uniform(0.2, 0.5)

    data = [
        [o1, h1, l1, c1],
        [o2, h2, l2, c2]
    ]
    return _df_multi(data)


# -----------------------------------------------------
# Helper Functions
# -----------------------------------------------------

def _create_df(open_price, high, low, close_price):
    """Creates a single-candle OHLC DataFrame."""
    return pd.DataFrame({
        "open": [open_price],
        "high": [high],
        "low": [low],
        "close": [close_price]
    })


def _df_multi(data_list):
    """Creates multi-candle DataFrame for 2–3 candle patterns."""
    o, h, l, c = [], [], [], []
    for row in data_list:
        o.append(row[0])
        h.append(row[1])
        l.append(row[2])
        c.append(row[3])

    return pd.DataFrame({
        "open": o,
        "high": h,
        "low": l,
        "close": c
    })


# -----------------------------------------------------
# Pattern Selector
# -----------------------------------------------------
def get_pattern(name):
    patterns = {
        "Doji": generate_doji,
        "Hammer": generate_hammer,
        "Shooting Star": generate_shooting_star,
        "Bullish Engulfing": generate_bullish_engulfing,
        "Bearish Engulfing": generate_bearish_engulfing,
    }
    return patterns[name]()

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
# TRAINING GAME PAGE — PATTERN PREVIEW ADDED HERE
# -----------------------------------------------------

elif page == "Training Game":
    st.title("🕹️ Training Game")
    st.write("Select a candlestick pattern to preview it. More game mechanics coming soon!")

    # Dropdown for selecting which pattern to show
    pattern_choice = st.selectbox(
        "Choose a pattern:",
        ["Doji", "Hammer", "Shooting Star", "Bullish Engulfing", "Bearish Engulfing"]
    )

    # Generate data using the selected pattern
    df = patterns.get_pattern(pattern_choice)

    st.subheader(f"Pattern Preview: {pattern_choice}")

    # --------------------
    # Plotly Candlestick Chart
    # --------------------
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

    st.success("This pattern generator is now working. Training logic comes next!")

# -----------------------------------------------------
# STATISTICS PAGE
# -----------------------------------------------------

elif page == "Statistics":
    st.title("📊 Statistics")
    st.write("Your accuracy and progress will appear here once the full game is built.")


