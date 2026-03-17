import streamlit as st

def show_home():

    st.set_page_config(layout="wide")

    # ---------------- HEADER ----------------
    st.title("🏏 Cricbuzz LiveStats Dashboard")

    st.markdown("""
    Welcome to **Cricbuzz LiveStats** — a real-time cricket analytics platform  
    powered by **Streamlit, MySQL, and Cricbuzz API**.
    """)

    st.markdown("---")

    #  FEATURES 
    st.subheader("🚀 Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📡 Live Match Insights
        - Real-time scores  
        - Batting & Bowling stats  
        - Match status & venue  
        """)

        st.markdown("""
        ### 📊 Top Player Stats
        - Most Runs leaderboard  
        - Best performances  
        - Player rankings  
        """)

    with col2:
        st.markdown("""
        ### 🧮 SQL Analytics
        - 25+ SQL queries  
        - Beginner → Advanced  
        - Cricket insights  
        """)

        st.markdown("""
        ### 🛠 CRUD Operations
        - Add players  
        - Update stats  
        - Delete records  
        """)

    st.markdown("---")

    #  NAVIGATION GUIDE 
    st.subheader("🧭 Navigation Guide")

    st.info("""
    Use the sidebar to navigate between pages:

    👉 Live Match → Real-time match data  
    👉 Top Player Stats → Leaderboards  
    👉 SQL Analytics → Query insights  
    👉 CRUD Operations → Manage database  
    """)

    st.markdown("---")

    #  HIGHLIGHTS 
    st.subheader("⭐ Project Highlights")

    col1, col2, col3 = st.columns(3)

    col1.metric("📊 SQL Queries", "25+")
    col2.metric("🏏 API Integration", "Real-Time")
    col3.metric("⚡ Performance", "Fast & Interactive")

    st.markdown("---")

    #  FOOTER 
    st.markdown("""
    👨‍💻 Developed by **ramesh krishna**  
    🚀 Built using Python, Streamlit, MySQL  
    """)