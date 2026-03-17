import streamlit as st
import pandas as pd
from utils.db_connection import get_connection

def show_sql_queries():

    st.title("🏏 SQL Analytics 📊")

    conn = get_connection()
    #st.write("Connection:", conn)

    #All questions and SQL queries
    queries = {

    "1. Find all players who represent India":

    """
        SELECT 
            name AS full_name,
            playing_role,
            batting_style,
            bowling_style
        FROM players
        WHERE country = 'India';
        """,

    "2. Find all cricket matches that were played in the last Few days":

    """
        SELECT
            series_name,
            team1, team2,
            venue, venue_city,
            start_date 
            from recent_matches 
            order by start_date desc;
            """,

    "3. Find the top 10 highest run scorers in ODI cricket":

    """
    SELECT
        player_name,
        runs AS total_runs_scored,
        batting_average,
        centuries
    FROM odi_player_stats
    ORDER BY CAST(runs AS UNSIGNED) DESC
    LIMIT 10;
    """,

    "4. Display all cricket venues that have a seating capacity of more than 25,000 spectators":

    """
    SELECT 
        ground,city,
        country,capacity FROM venue 
        WHERE capacity >25000 
        order by capacity desc;
    """,

    "5. Count matches each team has won":

    """
    SELECT 
    TRIM(SUBSTRING(result, 1, LOCATE(' won', result) - 1)) AS team_name,
    COUNT(*) AS total_wins
    FROM recent_matches
    WHERE result LIKE '% won%'
    GROUP BY team_name
    ORDER BY total_wins DESC;
    """,

    "6. Find how many players belong to each playing role":

    """
    SELECT 
    playing_role,
    COUNT(*) AS total_players
    FROM players
    GROUP BY playing_role
    ORDER BY total_players DESC;
    """,

    "7. Find the highest individual batting score achieved in each cricket format":

    """
    SELECT 'Test' AS format, player_name, highest_score
    FROM test_player_stats
    WHERE highest_score = (SELECT MAX(highest_score) FROM test_player_stats)

    UNION

    SELECT 'ODI', player_name, highest_score
    FROM odi_player_stats
    WHERE highest_score = (SELECT MAX(highest_score) FROM odi_player_stats)

    UNION
    SELECT 'T20I', player_name, highest_score
    FROM t20i_player_stats
    WHERE highest_score = (SELECT MAX(highest_score) FROM t20i_player_stats);
    """,

    "8. Find all cricket series that started in the year 2024":

    """
    SELECT 
        series_name,

        TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(series_name, 'tour of', -1), ',', 1)) AS host_country,

        CASE
            WHEN series_name LIKE '%Test%' THEN 'Test'
            WHEN series_name LIKE '%ODI%' OR series_name LIKE '%One-Day%' THEN 'ODI'
            WHEN series_name LIKE '%T20%' THEN 'T20'
            ELSE 'Mixed'
        END AS match_type,

        start_date

    FROM series_archieves
    WHERE series_name LIKE '%tour of%'
    AND YEAR(start_date) = 2024;""",

    "9. Find all-rounder players who have scored more than 1000 runs AND taken more than 50 wickets in their career":

    """
    SELECT 
        bat.player_name,
        bat.runs,
        b.wickets,
        'ODI' AS format
    FROM odi_player_stats bat
    JOIN odi_bowling_stats b
        ON bat.player_id = b.player_id
    JOIN players p
        ON bat.player_id = p.player_id
    WHERE bat.runs > 1000
    AND b.wickets > 50
    AND p.playing_role = 'All-rounder';
    """,

    "10. Get details of the last 20 completed matches":

    """
    SELECT 
        match_desc AS match_description,
        team1 AS team1_name,
        team2 AS team2_name,
        
        TRIM(SUBSTRING_INDEX(result,' won',1)) AS winning_team,
        
        SUBSTRING_INDEX(SUBSTRING_INDEX(result,'by ', -1),' ',1) AS victory_margin,
        
        CASE
            WHEN result LIKE '%runs%' THEN 'runs'
            WHEN result LIKE '%wkts%' THEN 'wickets'
            ELSE 'N/A'
        END AS victory_type,
        
        venue AS venue_name

    FROM recent_matches
    WHERE result LIKE '%won%'
    ORDER BY start_date DESC
    LIMIT 20;
    """,

    "11. Compare each player's performance across different cricket formats":

    """
    SELECT 
        p.name AS player_name,

        t.runs AS test_runs,
        o.runs AS odi_runs,
        t20.runs AS t20i_runs,

        t.batting_average AS test_avg,
        o.batting_average AS odi_avg,
        t20.batting_average AS t20i_avg

    FROM players p

    LEFT JOIN test_player_stats t
        ON p.player_id = t.player_id
    LEFT JOIN odi_player_stats o
        ON p.player_id = o.player_id
    LEFT JOIN t20i_player_stats t20
        ON p.player_id = t20.player_id

    WHERE 
        (t.player_id IS NOT NULL) +
        (o.player_id IS NOT NULL) +
        (t20.player_id IS NOT NULL) >= 2;
        """,


    "12. team's performance when playing at home versus playing away":

    """SELECT 
        t.team_name,
        SUM(
            CASE 
                WHEN v.country = t.country THEN 1 
                ELSE 0 
            END
        ) AS home_wins,
        SUM(
            CASE 
                WHEN v.country != t.country THEN 1 
                ELSE 0 
            END
        ) AS away_wins
    FROM recent_matches m
    JOIN teams t 
        ON TRIM(SUBSTRING_INDEX(m.result,' won',1)) = t.team_name

    JOIN venue v 
        ON m.venue = v.ground

    WHERE m.result LIKE '%won%'

    GROUP BY t.team_name
    ORDER BY t.team_name;
    """,


    "13. Identify batting partnerships where two consecutive batsmen":

    """
    SELECT 
        b1.player_name AS batsman1,
        b2.player_name AS batsman2,
        (b1.runs + b2.runs) AS partnership_runs,
        b1.innings_id
    FROM batting_score b1
    JOIN batting_score b2
    ON b1.match_id = b2.match_id
    AND b1.innings_id = b2.innings_id
    AND b2.batting_position = b1.batting_position + 1
    WHERE (b1.runs + b2.runs) >= 100
    ORDER BY partnership_runs DESC;
    """,


    "14. Examine bowling performance at different venues":

    """
    SELECT 
        b.player_name AS bowler,
        v.ground AS venue,
        v.city,
        COUNT(DISTINCT b.match_id) AS matches_played,
        SUM(b.runs) AS runs_conceded,
        SUM(b.wickets) AS total_wickets,
        ROUND(AVG(b.economy),2) AS avg_economy_rate
    FROM bowling_scorecard b
    JOIN venue v
    ON b.venue_id = v.venueId
    WHERE b.overs >= 4
    GROUP BY b.player_name, v.ground, v.city
    ORDER BY total_wickets DESC;
    """,

    "15. Players consistent scoring":
    """SELECT 
        b.player_name,
        COUNT(*) AS close_matches_played,
        ROUND(AVG(b.runs),2) AS avg_runs_in_close_matches,
        SUM(CASE WHEN rm.result LIKE CONCAT(b.team_name,' won%') THEN 1 ELSE 0 END) AS wins_when_batting
    FROM batting_scorecard b
    JOIN recent_matches rm
    ON rm.match_id IN (
        SELECT match_id
        FROM recent_matches
        WHERE 
            (
                result LIKE '%runs%'
                AND CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(result,'by ',-1),' runs',1) AS UNSIGNED) < 50
            )
            OR
            (
                result LIKE '%wickets%'
                AND CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(result,'by ',-1),' wickets',1) AS UNSIGNED) < 5
            )
    )
    GROUP BY b.player_name
    ORDER BY avg_runs_in_close_matches DESC limit 3;
    """,


    "16. Yearly batting performance trends":

    """
    SELECT 
        player_id AS playerid,
        player_name AS name,
        SUM(runs) AS runs,
        ROUND(AVG(runs),2) AS batting_avg,
        ROUND((SUM(runs) / SUM(balls)) * 100,2) AS strike_rate,

        ROUND(
            (AVG(runs) * 0.6) + 
            ((SUM(runs) / SUM(balls)) * 100 * 0.4)
        ,2) AS batting_score,

        RANK() OVER (
            ORDER BY 
            ((AVG(runs) * 0.6) + ((SUM(runs) / SUM(balls)) * 100 * 0.4)) DESC
        ) AS batting_rank

    FROM batting_scorecard
    GROUP BY player_id, player_name
    ORDER BY batting_rank
    LIMIT 10;
    """,


    "17. Toss win advantage":

    """
    SELECT 
        toss_winner,
        match_winner,
        decision,
        COUNT(*) AS total_matches,
        ROUND(
            SUM(CASE WHEN toss_winner = match_winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
            2
        ) AS win_percentage
    FROM tossanalysis
    GROUP BY toss_winner, match_winner, decision
    ORDER BY decision;
    """,

    "18. Find the most economical bowlers in limited-overs cricket":
    """
    SELECT 
        player_name,
        COUNT(DISTINCT match_id) AS matches_played,
        SUM(wickets) AS total_wickets,
        ROUND(SUM(runs)/SUM(overs),2) AS economy_rate
    FROM bowling_facts
    GROUP BY player_name
    HAVING matches_played >= 10
    AND AVG(overs) >= 2
    ORDER BY economy_rate ASC;
    """,


    "19. Most consistent batsmen in Scoring":

    """
    SELECT 
        player_name,
        COUNT(*) AS innings_played,
        ROUND(AVG(runs),2) AS avg_runs,
        ROUND(STDDEV(runs),2) AS run_std_deviation
    FROM batting_facts
    WHERE balls >= 10
    AND match_year >= 2022
    GROUP BY player_name
    HAVING AVG(runs) > 50
    AND STDDEV(runs) > 0.5
    ORDER BY run_std_deviation ASC limit 10;
    """,

    "20. how many matches played across formats":
    """SELECT 
        p.name AS player_name,

        COALESCE(t.matches,0) AS test_matches,
        COALESCE(o.matches,0) AS odi_matches,
        COALESCE(t20.matches,0) AS t20_matches,

        t.batting_average AS test_avg,
        o.batting_average AS odi_avg,
        t20.batting_average AS t20_avg,

        (COALESCE(t.matches,0) +
        COALESCE(o.matches,0) +
        COALESCE(t20.matches,0)) AS total_matches

    FROM players p

    LEFT JOIN test_player_stats t
    ON p.player_id = t.player_id

    LEFT JOIN odi_player_stats o
    ON p.player_id = o.player_id

    LEFT JOIN t20i_player_stats t20
    ON p.player_id = t20.player_id

    WHERE 
        (COALESCE(t.matches,0) +
        COALESCE(o.matches,0) +
        COALESCE(t20.matches,0)) >= 20

    ORDER BY total_matches DESC;""",


    "21. Comprehensive performance ranking system for players":

    """SELECT 
        p.name AS player_name,

        o.runs,
        o.batting_average,
        b.wickets,

        -- Batting points
        ((o.runs * 0.01) +
        (o.batting_average * 0.5)) AS batting_points,

        -- Bowling points
        (b.wickets * 2) AS bowling_points,

        -- Total performance score
        (
            (o.runs * 0.01) +
            (o.batting_average * 0.5) +
            (b.wickets * 2)
        ) AS total_performance_score

    FROM players p

    LEFT JOIN odi_player_stats o
    ON p.player_id = o.player_id

    LEFT JOIN odi_bowling_stats b
    ON p.player_id = b.player_id

    ORDER BY total_performance_score DESC limit 1;""",


    "22. head-to-head match prediction analysis between teams":

    """SELECT 
        team1,
        team2,
        COUNT(*) AS total_matches,

        -- Wins
        SUM(CASE WHEN winning_team = team1 THEN 1 ELSE 0 END) AS team1_wins,
        SUM(CASE WHEN winning_team = team2 THEN 1 ELSE 0 END) AS team2_wins,

        -- Win Percentage
        ROUND(
            SUM(CASE WHEN winning_team = team1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),2
        ) AS team1_win_percentage,

        ROUND(
            SUM(CASE WHEN winning_team = team2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),2
        ) AS team2_win_percentage,

        -- Average Victory Margin
        ROUND(
            AVG(CASE WHEN winning_team = team1 THEN victory_margin END),2
        ) AS team1_avg_margin,

        ROUND(
            AVG(CASE WHEN winning_team = team2 THEN victory_margin END),2
        ) AS team2_avg_margin,

        -- Batting First Performance
        SUM(
            CASE 
            WHEN toss_decision = 'Bat' AND winning_team = team1 THEN 1 
            ELSE 0 
            END
        ) AS team1_wins_batting_first,

        SUM(
            CASE 
            WHEN toss_decision = 'Bat' AND winning_team = team2 THEN 1 
            ELSE 0 
            END
        ) AS team2_wins_batting_first,

        -- Bowling First Performance
        SUM(
            CASE 
            WHEN toss_decision = 'Bowl' AND winning_team = team1 THEN 1 
            ELSE 0 
            END
        ) AS team1_wins_bowling_first,
        SUM(
            CASE 
            WHEN toss_decision = 'Bowl' AND winning_team = team2 THEN 1 
            ELSE 0 
            END
        ) AS team2_wins_bowling_first
    FROM head_to_head_matches
    WHERE match_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
    GROUP BY team1, team2 HAVING COUNT(*) >= 5
    ORDER BY total_matches DESC;
    """,

    "23. Analyze recent player form and momentum":

    """WITH recent_innings AS (
        SELECT 
            player_id,
            player_name,
            runs,
            strike_rate,
            innings_id,

            ROW_NUMBER() OVER(
                PARTITION BY player_id 
                ORDER BY innings_id DESC
            ) AS match_rank
        FROM batting_scorecard
    ),

    player_form AS (
        SELECT 
            player_id,
            player_name,

            ROUND(AVG(CASE WHEN match_rank <=5 THEN runs END),2) AS avg_runs_last5,
            ROUND(AVG(CASE WHEN match_rank <=10 THEN runs END),2) AS avg_runs_last10,
            ROUND(AVG(CASE WHEN match_rank <=10 THEN strike_rate END),2) AS recent_strike_rate,

            SUM(CASE WHEN match_rank <=10 AND runs >=50 THEN 1 ELSE 0 END) AS fifties_last10,

            ROUND(STDDEV(CASE WHEN match_rank <=10 THEN runs END),2) AS consistency_score,

            CASE
                WHEN AVG(CASE WHEN match_rank <=5 THEN runs END) >=50 
                    AND STDDEV(CASE WHEN match_rank <=10 THEN runs END) <20
                THEN 'Excellent Form'

                WHEN AVG(CASE WHEN match_rank <=5 THEN runs END) >=35
                    AND STDDEV(CASE WHEN match_rank <=10 THEN runs END) <25
                THEN 'Good Form'

                WHEN AVG(CASE WHEN match_rank <=5 THEN runs END) >=20
                THEN 'Average Form'

                ELSE 'Poor Form'
            END AS form_category

        FROM recent_innings
        GROUP BY player_id, player_name
    ),

    ranked_players AS (
        SELECT *,
            ROW_NUMBER() OVER(
                PARTITION BY form_category
                ORDER BY avg_runs_last5 DESC
            ) AS rank_in_category
        FROM player_form

        WHERE 
            avg_runs_last5 > 0
            AND avg_runs_last10 > 0
            AND recent_strike_rate > 0
            AND consistency_score > 0
    )

    SELECT *
    FROM ranked_players
    WHERE rank_in_category <= 3
    ORDER BY form_category, rank_in_category;
    """,

    "24. Study batting partnerships to identify the best player combination":

    """WITH ordered_batsmen AS (
        SELECT
            innings_id,
            player_id,
            player_name,
            runs,

            ROW_NUMBER() OVER(
                PARTITION BY innings_id
                ORDER BY player_id
            ) AS batting_pos

        FROM batting_scorecard
    ),

    partnerships AS (
        SELECT
            b1.player_name AS batsman1,
            b2.player_name AS batsman2,
            b1.innings_id,

            (b1.runs + b2.runs) AS partnership_runs

        FROM ordered_batsmen b1
        JOIN ordered_batsmen b2
            ON b1.innings_id = b2.innings_id
            AND b2.batting_pos = b1.batting_pos + 1
    ),

    partnership_stats AS (
        SELECT
            batsman1,
            batsman2,

            COUNT(*) AS total_partnerships,

            ROUND(AVG(partnership_runs),2) AS avg_partnership_runs,

            SUM(CASE 
                WHEN partnership_runs >= 50 THEN 1 
                ELSE 0 
            END) AS partnerships_over_50,

            MAX(partnership_runs) AS highest_partnership,

            ROUND(
                SUM(CASE WHEN partnership_runs >= 50 THEN 1 ELSE 0 END)
                * 100.0 / COUNT(*),2
            ) AS success_rate

        FROM partnerships
        GROUP BY batsman1, batsman2
    )
    SELECT *,
    RANK() OVER(
        ORDER BY success_rate DESC, avg_partnership_runs DESC
    ) AS partnership_rank

    FROM partnership_stats WHERE total_partnerships >= 2 ORDER BY partnership_rank limit 5;
    """,

    "25. time-series analysis of player performance evolution":

    """WITH match_sequence AS (
        SELECT
            player_id,
            player_name,
            runs,
            strike_rate,
            innings_id,

            ROW_NUMBER() OVER(
                PARTITION BY player_id
                ORDER BY innings_id
            ) AS match_num

        FROM batting_scorecard
    ),

    quarter_groups AS (
        SELECT
            player_id,
            player_name,
            runs,
            strike_rate,
            innings_id,
            CEIL(match_num / 3) AS quarter_id
        FROM match_sequence
    ),

    quarter_stats AS (
        SELECT
            player_id,
            player_name,
            quarter_id,
            COUNT(*) AS matches_played,
            ROUND(AVG(runs),2) AS avg_runs,
            ROUND(AVG(strike_rate),2) AS avg_strike_rate
        FROM quarter_groups
        GROUP BY player_id, player_name, quarter_id
    ),

    quarter_trend AS (
        SELECT
            player_id,
            player_name,
            quarter_id,
            avg_runs,
            avg_strike_rate,

            LAG(avg_runs) OVER(
                PARTITION BY player_id
                ORDER BY quarter_id
            ) AS prev_runs

        FROM quarter_stats
    )

    SELECT
        player_id,
        player_name,
        quarter_id,
        avg_runs,
        avg_strike_rate,

        CASE

            WHEN avg_runs > prev_runs THEN 'Improving'
            WHEN avg_runs < prev_runs THEN 'Declining'
            ELSE 'Stable'
        END AS performance_trend

    FROM quarter_trend
    ORDER BY player_id, quarter_id;
    """
    }

    # Dropdown with all 25 questions
    selected_query = st.selectbox(
    "choose",
    list(queries.keys())
    )

    # Run query
    query = queries[selected_query]

    df = pd.read_sql(query, conn)

    st.subheader("Query 🔎")
    st.dataframe(df,use_container_width=True)
