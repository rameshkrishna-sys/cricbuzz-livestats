import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv
from utils.db_connection import get_connection


load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

HEADERS = {
    "x-rapidapi-key": "7cde9c129fmsh43ac0b206d50ebdp121f9cjsnfa25cdc2fd16",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"



# API FUNCTIONS (CACHED)


@st.cache_data
def search_players(name):

    url = f"{BASE_URL}/stats/v1/player/search"

    response = requests.get(url, headers=HEADERS, params={"plrN": name})

    if response.status_code == 200:
        return response.json()

    return {}


@st.cache_data
def get_player_details(player_id):

    url = f"{BASE_URL}/stats/v1/player/{player_id}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()

    return {}


@st.cache_data
def get_player_stats(player_id, stat_type):

    url = f"{BASE_URL}/stats/v1/player/{player_id}/{stat_type}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()

    return {}



# JSON → TABLE


def parse_stats_table(stats_json):

    if "headers" not in stats_json or "values" not in stats_json:
        return pd.DataFrame()

    headers = stats_json["headers"]

    rows = []

    for row in stats_json["values"]:
        rows.append(row["values"])

    df = pd.DataFrame(rows, columns=headers)

    return df




#  STREAMLIT PAGE 

def show_player_stats():

    st.title("📊 Player Profile")

    # SEARCH BOX WITH EXAMPLE TEXT
    search = st.text_input(
        "Search Player",
        placeholder="e.g Rohit Sharma, Virat Kohli, Joe Root"
    )

    if not search:
        return

    results = search_players(search)

    if "player" not in results:
        st.warning("No players found")
        return

    players = {p["name"]: p for p in results["player"]}

    selected_name = st.selectbox("Select Player", list(players.keys()))

    player = players[selected_name]

    player_id = player["id"]

    details = get_player_details(player_id)

    # ---------------- PLAYER HEADER ----------------

    col1, col2 = st.columns([1,3])

    with col1:

        if "faceImageId" in player:
            img = f"http://i.cricketcb.com/stats/img/faceImages/{player['faceImageId']}.jpg"
            st.image(img, width=160)

    with col2:

        st.header(player["name"])
        st.write(f"Team: {player['teamName']}")
        st.write(f"Role: {details.get('role','N/A')}")
        st.write(f"Batting Style: {details.get('bat','N/A')}")
        st.write(f"Bowling Style: {details.get('bowl','N/A')}")

    # ---------------- TABS ----------------

    tab1, tab2, tab3 = st.tabs(
        ["👤 Profile", "🏏 Batting Stats", "⚡ Bowling Stats"]
    )

# ---------------- PROFILE TAB ----------------

    with tab1:

        st.markdown("## 🎯 Personal Information")

        col1, col2, col3 = st.columns(3)

        # -------- Cricket Details --------
        with col1:
            st.markdown("### 🏏 Cricket Details")

            st.write("Role:", details.get("role", "N/A"))
            st.write("Batting:", details.get("bat", "N/A"))
            st.write("Bowling:", details.get("bowl", "N/A"))
            st.write("International Team:", player.get("teamName", "N/A"))

        # -------- Personal Details --------
        with col2:
            st.markdown("### 📍 Personal Details")

            st.write("Date of Birth:", details.get("DoB", "N/A"))
            st.write("Birth Place:", details.get("birthPlace", "N/A"))
            st.write("Height:", details.get("height", "N/A"))

        # -------- Teams Played --------
        with col3:
            st.markdown("### 🏆 Teams Played For")

            teams = details.get("teams", "")

            if teams:
                team_list = teams.split(",")
                for t in team_list:
                    st.write(f"• {t.strip()}")
            else:
                st.write("N/A")

        st.markdown("---")

        if "id" in player:
            st.markdown(
                f"🔗 **Full Profile:** https://www.cricbuzz.com/profiles/{player['id']}"
            )

    # ---------------- BATTING TAB ----------------

    with tab2:

        st.subheader("🏏 Batting Career Statistics")

        batting = get_player_stats(player_id,"batting")

        df = parse_stats_table(batting)

        if df.empty:
            st.warning("No batting stats available")
        else:

        

            try:

                test = df["Test"]
                odi = df["ODI"]
                t20 = df["T20"]
                ipl = df["IPL"]

                col1,col2,col3,col4 = st.columns(4)

                with col1:
                    st.metric("Test Matches", test.iloc[0])
                    st.metric("Runs", test.iloc[2])
                    st.metric("Average", test.iloc[5])

                with col2:
                    st.metric("ODI Matches", odi.iloc[0])
                    st.metric("Runs", odi.iloc[2])
                    st.metric("Average", odi.iloc[5])

                with col3:
                    st.metric("T20 Matches", t20.iloc[0])
                    st.metric("Runs", t20.iloc[2])
                    st.metric("Average", t20.iloc[5])

                with col4:
                    st.metric("IPL Matches", ipl.iloc[0])
                    st.metric("Runs", ipl.iloc[2])
                    st.metric("Average", ipl.iloc[5])

            except:
                pass

    # ---------------- BOWLING TAB ----------------

    with tab3:

        st.subheader("🎯 Bowling Statistics")

        bowling = get_player_stats(player_id,"bowling")

        df = parse_stats_table(bowling)

        if df.empty:
            st.warning("No bowling stats available")

        else:

            try:

                test = df["Test"]
                odi = df["ODI"]
                t20 = df["T20"]
                ipl = df["IPL"]

                col1,col2,col3,col4 = st.columns(4)

                with col1:
                    st.metric("Test Wickets", test.iloc[4])
                    st.metric("Average", test.iloc[6])
                    st.metric("Economy", test.iloc[7])

                with col2:
                    st.metric("ODI Wickets", odi.iloc[4])
                    st.metric("Average", odi.iloc[6])
                    st.metric("Economy", odi.iloc[7])

                with col3:
                    st.metric("T20 Wickets", t20.iloc[4])
                    st.metric("Average", t20.iloc[6])
                    st.metric("Economy", t20.iloc[7])

                with col4:
                    st.metric("IPL Wickets", ipl.iloc[4])
                    st.metric("Average", ipl.iloc[6])
                    st.metric("Economy", ipl.iloc[7])

            except:
                pass


    # ---------------- SAVE PLAYER TO DATABASE ----------------

    if st.button("Save Player To Database"):

        conn = get_connection()

        cursor = conn.cursor()

        insert_query = """
        INSERT INTO players (player_id,name)
        VALUES (%s,%s)
        ON DUPLICATE KEY UPDATE name=VALUES(name)
        """

        cursor.execute(
            insert_query,
            (player_id,player["name"])
        )

        conn.commit()

        cursor.close()
        conn.close()

        st.success("Player saved to database")