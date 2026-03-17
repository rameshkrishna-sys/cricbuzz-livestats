import streamlit as st
import os  # 👈 ADD THIS

# 🔍 DEBUG (ADD THIS BLOCK)
#st.write("CURRENT PATH:", os.getcwd())

# Page settings
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

# Sidebar
st.sidebar.title("🏏 Cricbuzz LiveStats")

page = st.sidebar.selectbox(
    "Select Page",
    ["Home", "Live Matches", "Player Profile", "SQL Queries", "CRUD"]
)

# LOAD PAGES 

if page == "Home":
    from modules.home import show_home
    show_home()

elif page == "Live Matches":
    from modules.live_matches import show_live_matches
    show_live_matches()

elif page == "Player Profile":
    from modules.player_stats import show_player_stats
    show_player_stats()

elif page == "SQL Queries":
    from modules.sql_queries import show_sql_queries
    show_sql_queries()

elif page == "CRUD":
    from modules.crud_operations import show_crud
    show_crud()