import streamlit as st
import pandas as pd
import sys
from pathlib import Path

from src.data.data_processing import run_data_processing_pipeline
from src.analysis.poisson import calc_poisson_for_all_teams


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
        team_data, team_players, df_matches, df_match_data = run_data_processing_pipeline(use_table=use_table, league=league, season=season)

    
    if not team_data:
        st.warning("Keine verarbeiteten Team-Daten vorhanden.")
        return
    st.success("Aufbereitete Daten erfolgreich geladen!")
    
    # Alle Teams sortiert auflisten
    teams = sorted(team_data.keys())
    
    
        # ----------------------
        # EINZELTEAM-ANSICHT
        # ----------------------
    selected_team = st.selectbox("Team auswählen:", teams)
        
    st.subheader(f"Statistiken für {selected_team}")
    stats = team_data[selected_team]["stats"]
        
        # Als DataFrame für eine übersichtliche Darstellung
    stats_df = pd.DataFrame([stats], index=[selected_team]).T
    st.dataframe(stats_df)  # dataFrame statt table -> scrollbar
        # Club Logo
    icon_url = stats_df[selected_team]["teamIconUrl"]
        # Statistiken
    wins = stats_df[selected_team]["won"]
    lost = stats_df[selected_team]["lost"]
    draw = stats_df[selected_team]["draw"]
    goalDifference = stats_df[selected_team]["goalDiff"]
    goals = stats_df[selected_team]["goals"]
    goalsAgainst = stats_df[selected_team]["opponentGoals"]
    points = stats_df[selected_team]["points"]
    st.write("### Statistiken")
    st.write(f"Anzahl Spiele: {stats_df[selected_team]['matches']}")
    st.write(f"Anzahl Unentschieden: {draw}")
    st.write(f"Torverhältnis: {goals} : {goalsAgainst} ({goalDifference})")
    st.write(f"Punkte: {points}")
    st.write(f"Anzahl Niederlagen: {lost}")
    st.write(f"Anzahl Siege: {wins}")
    st.image(icon_url, caption=f"Logo: {selected_team}",width=200)
        # Nur im klassischen Modus gibt es Match-Daten
    if not use_table:
        if st.checkbox("Spieldaten anzeigen"):
            st.subheader("Rohdaten der Spiele")
            st.dataframe(team_data[selected_team]["matches"])
        
    st.subheader("Spielerdaten")
    if selected_team in team_players:
        st.dataframe(team_players[selected_team])
    else:
        st.info(f"Keine Spielerdaten für {selected_team} gefunden.")
    

if __name__ == "__main__":
    main()

