import streamlit as st
import pandas as pd
from utils.db_connection import get_connection


def show_crud():

    st.title("🛠 CRUD Operations")
    st.markdown("✏️ **Create, Read, Update, Delete Player Records**")

    conn = get_connection()

    if conn is None:
        st.error("❌ Database not available in deployed version")
        st.info("Run this feature locally to use CRUD operations")
        return  

    cursor = conn.cursor()  

    option = st.selectbox(
        "Choose an operation:",
        ["📖Read (View Players)", "➕Create (Add Player)", "✏️Update (Edit Player)", "🗑Delete (Remove Player)"]
    )
    st.write("Selected:", option)

    #  READ 
    if option == "📖Read (View Players)":

        st.subheader("📖 View All Players")

        col1, col2 = st.columns([1,2])

        with col1:
            load_btn = st.button("📊 Load All Players")

        with col2:
            search = st.text_input("🔍 Search player by name")

        if load_btn:

            query = """
            SELECT * FROM most_run_stats
            ORDER BY runs DESC
            """

            df = pd.read_sql(query, conn)

            st.success(f"✅ Found {len(df)} players in database")

            if search:
                df = df[df["player_name"].str.contains(search, case=False)]

            st.dataframe(df, use_container_width=True)

    # ---------------- CREATE ----------------
    elif option == "➕Create (Add Player)":

        st.subheader("➕ Add New Player")

        col1, col2 = st.columns(2)

        with col1:
            player_id = st.number_input("Player ID", step=1)
            name = st.text_input("Player Name")
            matches = st.number_input("Matches", step=1)

        with col2:
            innings = st.number_input("Innings", step=1)
            runs = st.number_input("Runs", step=1)
            avg = st.number_input("Average")

        if st.button("➕ Add Player"):

            cursor.execute("""
                INSERT INTO most_run_stats
                (player_id, player_name, matches, innings, runs, average)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE player_name=VALUES(player_name)
            """, (player_id, name, matches, innings, runs, avg))

            conn.commit()

            st.success("✅ Player Added Successfully")

    #  UPDATE 
    elif option == "✏️Update (Edit Player)":

        st.subheader("✏ Update Player Information")

        # 🔍 Search
        search = st.text_input("🔍 Search player to update")

        if search:

            df = pd.read_sql(
                f"SELECT * FROM most_run_stats WHERE player_name LIKE '%{search}%'",
                conn
            )

            if not df.empty:

                # 🎯 Select player
                selected = st.selectbox(
                    "Select player to update:",
                    df["player_name"] + " (ID: " + df["player_id"].astype(str) + ")"
                )

                # Extract player_id from selection
                player_id = int(selected.split("ID: ")[1].replace(")", ""))

                player_data = df[df["player_id"] == player_id].iloc[0]

                #  CURRENT INFO 
                st.markdown("### Current Information:")

                st.info(
                    f"Name: {player_data['player_name']} | "
                    f"Matches: {player_data['matches']} | "
                    f"Runs: {player_data['runs']} | "
                    f"Average: {player_data['average']}"
                )

                #  NEW INFO CARD 
                st.markdown("### New Information:")

                with st.container():

                    col1, col2 = st.columns(2)

                    with col1:
                        new_name = st.text_input(
                            "Player Name",
                            value=str(player_data["player_name"])
                        )

                        matches = st.number_input(
                            "Matches",
                            value=int(player_data["matches"]),
                            step=1
                        )

                        innings = st.number_input(
                            "Innings",
                            value=int(player_data["innings"]),
                            step=1
                        )

                    with col2:
                        runs = st.number_input(
                            "Runs",
                            value=int(player_data["runs"]),
                            step=1
                        )

                        avg = st.number_input(
                            "Average",
                            value=float(player_data["average"]),
                            step=0.1
                        )

                #  UPDATE BUTTON 
                if st.button("✏️ Update Player"):

                    cursor.execute("""
                        UPDATE most_run_stats
                        SET player_name=%s,
                            matches=%s,
                            innings=%s,
                            runs=%s,
                            average=%s
                        WHERE player_id=%s
                    """, (
                        str(new_name),
                        int(matches),
                        int(innings),
                        int(runs),
                        float(avg),
                        int(player_id)
                    ))

                    conn.commit()

                    st.success("✅ Player Updated Successfully")

            else:
                st.warning("No player found")
    #  DELETE 
    elif option == "🗑Delete (Remove Player)":

        st.subheader("🗑 Delete Player Record")

        st.warning("⚠️ This action cannot be undone!")

        search = st.text_input("🔍 Search player to delete")

        if search:

            df = pd.read_sql(
                f"SELECT * FROM most_run_stats WHERE player_name LIKE '%{search}%'",
                conn
            )

            if not df.empty:

                selected = st.selectbox(
                    "Select player to DELETE:",
                    df["player_name"]
                )

                player_data = df[df["player_name"] == selected].iloc[0]

                st.error(f"⚠️ You are about to delete: {selected}")

                confirm = st.text_input(f"Type 'DELETE {selected}' to confirm:")

                if confirm == f"DELETE {selected}":

                    if st.button("Confirm Deletion"):

                        cursor.execute(
                            "DELETE FROM most_run_stats WHERE player_id=%s",
                            (int(player_data["player_id"]),)
                            )
                        

                        conn.commit()

                        st.success("🗑 Player Deleted Successfully")

            else:
                st.warning("No player found")

    cursor.close()
    conn.close()