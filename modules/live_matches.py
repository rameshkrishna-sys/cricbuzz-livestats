import requests
import streamlit as st
import pandas as pd
from config import Config


#  FETCH MATCHES 
@st.cache_data(ttl=3600)
def fetch_matches():

    headers = {
        "x-rapidapi-key": Config.RAPIDAPI_KEY,
        "x-rapidapi-host": Config.RAPIDAPI_HOST
    }

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if "message" in data:
            return {"error": data["message"]}

        match_dict = {}

        for match_type in data.get("typeMatches", []) or []:
            for series_item in match_type.get("seriesMatches", []):

                if "seriesAdWrapper" not in series_item:
                    continue

                matches = series_item["seriesAdWrapper"].get("matches", [])

                for match in matches:
                    info = match.get("matchInfo", {})

                    team1 = info.get("team1", {}).get("teamName", "")
                    team2 = info.get("team2", {}).get("teamName", "")
                    series_name = info.get("seriesName", "")

                    key = f"{team1} vs {team2}, {series_name}"

                    match_dict[key] = match

        return match_dict

    except Exception as e:
        return {"error": str(e)}


#  FETCH SCORECARD 
@st.cache_data(ttl=3600)
def fetch_scorecard(match_id):

    headers = {
        "x-rapidapi-key": Config.RAPIDAPI_KEY,
        "x-rapidapi-host": Config.RAPIDAPI_HOST
    }

    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"

    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


#  MAIN FUNCTION 
def show_live_matches():
    st.title("📡 Cricbuzz Live Match Dashboard")



    # 🔍 DEBUG (remove later)
    #st.write("API KEY:", Config.RAPIDAPI_KEY)

    #  FETCH MATCHES 
    with st.spinner("Fetching matches..."):
        result = fetch_matches()

    if isinstance(result, dict) and "error" in result:
        st.error(f"❌ API Error: {result['error']}")
        st.info("💡 Check API key or rate limit")
        return

    if not result:
        st.warning("⚠️ No matches available")
        return

    #  SELECT MATCH 
    selection = st.selectbox("Select Match", list(result.keys()))

    match = result[selection]
    match_info = match.get("matchInfo", {})
    match_score = match.get("matchScore", {})
    match_id = match_info.get("matchId")

    #  HEADER 
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(
            f"## 🏏 {match_info.get('team1', {}).get('teamName')} vs {match_info.get('team2', {}).get('teamName')}"
        )

        st.write(f"📄 Match: {match_info.get('matchDesc')}")
        st.write(f"🏆 Format: {match_info.get('matchFormat')}")
        st.write(f"🏟 Venue: {match_info.get('venueInfo', {}).get('ground')}")
        st.write(f"📍 City: {match_info.get('venueInfo', {}).get('city')}")
        st.write(f"📌 Status: {match_info.get('status')}")

    with col2:
        st.info(f"📅 Series: {match_info.get('seriesName')}")

    #  STATUS 
    st.subheader("📊 Match Result / Current Status")
    st.success(match_info.get("status"))

    #  SCORE 
    st.divider()
    st.subheader("📊 Current Score")

    col1, col2 = st.columns(2)

    with col1:
        team1_score = match_score.get("team1Score", {}).get("inngs1", {})
        st.markdown(f"### {match_info.get('team1', {}).get('teamSName')}")
        st.write(f"{team1_score.get('runs', 0)}/{team1_score.get('wickets', 0)}")
        st.write(f"{team1_score.get('overs', 0)} overs")

    with col2:
        team2_score = match_score.get("team2Score", {}).get("inngs1", {})
        st.markdown(f"### {match_info.get('team2', {}).get('teamSName')}")
        st.write(f"{team2_score.get('runs', 0)}/{team2_score.get('wickets', 0)}")
        st.write(f"{team2_score.get('overs', 0)} overs")

    #  SCORECARD 
    st.divider()
    st.subheader("📋 Detailed Scorecard")

    if not match_id:
        st.warning("No scorecard available")
        return

    with st.spinner("Fetching scorecard..."):
        score_card = fetch_scorecard(match_id)

    if isinstance(score_card, dict) and "error" in score_card:
        st.error(f"Scorecard Error: {score_card['error']}")
        return

    if "message" in score_card:
        st.error(score_card["message"])
        return

    scorecard = score_card.get("scorecard", [])

    if not scorecard:
        st.warning("Scorecard not available")
        return

    #  DISPLAY 
    for i, team_data in enumerate(scorecard[:2]):

        team_name = team_data.get("batteamname", f"Team {i+1}")

        with st.expander(f"🏏 {team_name}"):

            # Batting
            batters = pd.DataFrame(team_data.get("batsman", []))
            if not batters.empty:
                batters = batters[
                    ["name", "runs", "balls", "fours", "sixes", "strkrate", "outdec"]
                ]
                st.markdown("#### 🏏 Batting")
                st.dataframe(batters, use_container_width=True)
            else:
                st.write("No batting data")

            # Bowling
            bowlers = pd.DataFrame(team_data.get("bowler", []))
            if not bowlers.empty:
                bowlers = bowlers[
                    ["name", "overs", "maidens", "runs", "wickets", "economy"]
                ]
                st.markdown("#### 🎯 Bowling")
                st.dataframe(bowlers, use_container_width=True)
            else:
                st.write("No bowling data")