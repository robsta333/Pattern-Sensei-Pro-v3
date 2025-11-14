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
