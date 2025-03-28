import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from Code.API.data_processing import run_data_processing_pipeline


# Layout so setzen, dass Streamlit die volle Fensterbreite nutzt:
st.set_page_config(layout="wide", page_title="Bundesliga Dashboard")

def main():
    st.title("Bundesliga Dashboard (Prototyp)")
    
    # Sidebar: Einstellungen
    st.sidebar.header("Einstellungen")
    league = st.sidebar.selectbox("Liga", ["bl1"])  # Nur Bundesliga
    season = st.sidebar.text_input("Saison", "2024")
    use_table = st.sidebar.checkbox("Nur Tabelle anzeigen (OpenLigaDB)", value=True)
    
        
    with st.spinner("Verarbeite Daten..."):
        team_data, team_players = run_data_processing_pipeline(use_table=use_table, league=league, season=season)
    
    if not team_data:
        st.warning("Keine verarbeiteten Team-Daten vorhanden.")
        return
    st.success("Aufbereitete Daten erfolgreich geladen!")
    
    # Alle Teams sortiert auflisten
    teams = sorted(team_data.keys())

    st.subheader("Teamvergleich")
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Team 1 auswählen:", teams, key="team1")
        with col2:
            team2 = st.selectbox("Team 2 auswählen:", teams, key="team2")
        
    if team1 == team2:
        st.error("Bitte zwei unterschiedliche Teams auswählen.")
        return
    else:
        stats1 = team_data[team1]["stats"]
        stats2 = team_data[team2]["stats"]
        comp_df = pd.DataFrame([stats1, stats2], index=[team1, team2])
             # Als DataFrame für eine übersichtliche Darstellung
        stats_df1 = pd.DataFrame([stats1], index=[team1]).T
        stats_df2 = pd.DataFrame([stats2], index=[team2]).T

            # Club Logo
        icon_url = stats_df1[team1]["teamIconUrl"]
        # Statistiken Team1
        wins = stats_df1[team1]["won"]
        lost = stats_df1[team1]["lost"]
        draw = stats_df1[team1]["draw"]
        goalDifference = stats_df1[team1]["goalDiff"]
        goals = stats_df1[team1]["goals"]
        goalsAgainst = stats_df1[team1]["opponentGoals"]
        points = stats_df1[team1]["points"]
           

            # Club Logo
        icon_url = stats_df2[team2]["teamIconUrl"]
            # Statistiken
        wins = stats_df2[team2]["won"]
        lost = stats_df2[team2]["lost"]
        draw = stats_df2[team2]["draw"]
        goalDifference = stats_df2[team2]["goalDiff"]
        goals = stats_df2[team2]["goals"]
        goalsAgainst = stats_df2[team2]["opponentGoals"]
        points = stats_df2[team2]["points"]
           
            
    col1, col2 = st.columns(2)  # Erstelle zwei Spalten

    with col1:  # Linke Spalte für Team 1
            st.write(f"## {team1}")
            st.image(stats_df1[team1]["teamIconUrl"], caption=f"Logo: {team1}", width=200)
            st.divider()
            st.write(f"**Anzahl Spiele:** {stats_df1[team1]['matches']}")
            st.write(f"**Anzahl Unentschieden:** {stats_df1[team1]['draw']}")
            st.write(f"**Torverhältnis:** {stats_df1[team1]['goals']} : {stats_df1[team1]['opponentGoals']} ({stats_df1[team1]['goalDiff']})")
            st.write(f"**Punkte:** {stats_df1[team1]['points']}")
            st.write(f"**Anzahl Niederlagen:** {stats_df1[team1]['lost']}")
            st.write(f"**Anzahl Siege:** {stats_df1[team1]['won']}")

    with col2:  # Rechte Spalte für Team 2
            st.write(f"## {team2}")
            st.image(stats_df2[team2]["teamIconUrl"], caption=f"Logo: {team2}", width=200)
            st.divider()
            st.write(f"**Anzahl Spiele:** {stats_df2[team2]['matches']}")
            st.write(f"**Anzahl Unentschieden:** {stats_df2[team2]['draw']}")
            st.write(f"**Torverhältnis:** {stats_df2[team2]['goals']} : {stats_df2[team2]['opponentGoals']} ({stats_df2[team2]['goalDiff']})")
            st.write(f"**Punkte:** {stats_df2[team2]['points']}")
            st.write(f"**Anzahl Niederlagen:** {stats_df2[team2]['lost']}")
            st.write(f"**Anzahl Siege:** {stats_df2[team2]['won']}")


            
            
            # Du kannst hier auswählen, welche Spalten du anzeigen möchtest:
            columns_of_interest = [
                "matches", "wins", "draws", "losses",
                "goals_scored", "goals_conceded", "goal_difference", "points",
                # xG-Metriken:
                "avg_xG", "avg_xGA", "avg_npxG", "avg_npxGA",
                "avg_ppda_att", "avg_ppda_def"
            ]
            # Nur Spalten anzeigen, die tatsächlich existieren
            available_cols = [c for c in columns_of_interest if c in comp_df.columns]
            comp_df_display = comp_df[available_cols]
            
            st.title("Vergleich der Teams")

            #st.dataframe(comp_df)

    tab1, tab2, tab3 = st.tabs(["Siege", "Punkte", "Torhistorie"])
            
    with tab1:
        st.subheader("Siege")
                
            # Falls du alle (o. g. selektierten) numerischen Spalten plotten willst:
        if not comp_df_display.empty:
                    st.bar_chart(comp_df["won"])
        else:
                    st.info("Keine numerischen Kennzahlen zum Vergleich vorhanden.")
            
        with tab2:
                st.subheader("Punkte")
                if not comp_df_display.empty:
                    st.bar_chart(comp_df_display["points"])
                else:
                    st.info("Keine numerischen Kennzahlen zum Vergleich vorhanden.")
            
        with tab3:
                st.subheader("Torhistorie")
                if not comp_df_display.empty:
                    st.line_chart(comp_df[["goals_scored", "goals_conceded"]])
                else:
                    st.info("Keine numerischen Kennzahlen zum Vergleich vorhanden.")

            
                

            
            
            # Optional: Vergleich der Roh-Spieldaten (nur im klassischen Modus sinnvoll)
        if not use_table:
                show_match_data = st.checkbox("Spieldaten anzeigen", value=False, key="matchdata_compare")
                if show_match_data:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Spieldaten für {team1}")
                        st.dataframe(team_data[team1]["matches"])
                    with col2:
                        st.write(f"Spieldaten für {team2}")
                        st.dataframe(team_data[team2]["matches"])
            
            # Spielerdatenvergleich
        st.subheader("Spielerdaten Vergleich")
        col1, col2 = st.columns(2)
        with col1:
                st.write(f"Spielerdaten für {team1}")
                if team1 in team_players:
                    st.dataframe(team_players[team1])
                else:
                    st.info(f"Keine Spielerdaten für {team1} gefunden.")
        with col2:
                st.write(f"Spielerdaten für {team2}")
                if team2 in team_players:
                    st.dataframe(team_players[team2])
                else:
                    st.info(f"Keine Spielerdaten für {team2} gefunden.")
                
if __name__ == "__main__":
    main()
