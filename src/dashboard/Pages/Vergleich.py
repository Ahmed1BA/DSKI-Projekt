import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from src.data.data_processing import run_data_processing_pipeline
from src.analysis.poisson import calc_poisson_for_all_teams


# Layout so setzen, dass Streamlit die volle Fensterbreite nutzt:
st.set_page_config(layout="wide", page_title="Bundesliga Dashboard")
def score_matrix(dist_home, dist_away):
    return np.outer(dist_home, dist_away)

def over_under(sm, threshold):
    t = int(threshold + 0.5)
    total = 0
    for i in range(sm.shape[0]):
        for j in range(sm.shape[1]):
            if i + j >= t:
                total += sm[i, j]
    return total

def plot_score_heatmap(sm, team1, team2):
    fig, ax = plt.subplots()
    cax = ax.matshow(sm, cmap='Blues')
    ax.set_title(f"{team1} vs {team2}")
    ax.set_xlabel(team2)
    ax.set_ylabel(team1)
    plt.colorbar(cax)
    for (i, j), val in np.ndenumerate(sm):
        ax.text(j, i, f"{val:.2f}", va='center', ha='center', color='black')
    return fig

def main():
    st.title("Bundesliga Dashboard (Prototyp)")
    
    # Sidebar: Einstellungen
    st.sidebar.header("Einstellungen")
    league = st.sidebar.selectbox("Liga", ["bl1"])  # Nur Bundesliga
    season = st.sidebar.text_input("Saison", "2024")
    use_table = st.sidebar.checkbox("Nur Tabelle anzeigen (OpenLigaDB)", value=True)
    
        
    with st.spinner("Verarbeite Daten..."):
        team_data, team_players, df_matches, _ = run_data_processing_pipeline(use_table=False)

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

        st.write(f"**Team 1**: {team1}, **Team 2**: {team2}")
        m_between = df_matches[((df_matches['home_team_std'] == team1) & (df_matches['away_team_std'] == team2)) | ((df_matches['home_team_std'] == team2) & (df_matches['away_team_std'] == team1))]
        if m_between.empty:
            st.info("Keine direkten Duelle gefunden.")
        else:
            st.dataframe(m_between)
        stats1 = team_data[team1]["stats"]
        stats2 = team_data[team2]["stats"]
        comp_df = pd.DataFrame([stats1, stats2], index=[team1, team2])
             # Als DataFrame für eine übersichtliche Darstellung
        stats_df1 = pd.DataFrame([stats1], index=[team1]).T
        stats_df2 = pd.DataFrame([stats2], index=[team2]).T
        matches = team_data[team1]["matches"]
        matches2 = team_data[team2]["matches"]
       

            # Club Logo
      # Suche ein beliebiges Spiel, in dem das Team beteiligt ist
         

        # Statistiken Team1
        wins = stats_df1[team1]["wins"]
        lost = stats_df1[team1]["losses"]
        draw = stats_df1[team1]["draws"]
        goalDifference = stats_df1[team1]["goal_difference"]
        goals = stats_df1[team1]["goals_scored"]
        goalsAgainst = stats_df1[team1]["goals_conceded"]
        points = stats_df1[team1]["points"]
           

            # Club Logo
        # Suche ein beliebiges Spiel, in dem das Team beteiligt ist
        # Hier wird das erste Spiel des Teams verwendet, um das Logo zu finden
        # Beispiel: Verwende das erste Spiel des Teams
        icon_url1 = matches.iloc[0]["teams.home.logo"] if matches.iloc[0]["teams.home.name"] == team1 else matches.iloc[0]["teams.away.logo"]
        icon_url2 = matches2.iloc[0]["teams.home.logo"] if matches2.iloc[0]["teams.home.name"] == team2 else matches2.iloc[0]["teams.away.logo"]
            
            # Statistiken
        wins = stats_df2[team2]["wins"]
        lost = stats_df2[team2]["losses"]
        draw = stats_df2[team2]["draws"]
        goalDifference = stats_df2[team2]["goal_difference"]
        goals = stats_df2[team2]["goals_scored"]
        goalsAgainst = stats_df2[team2]["goals_conceded"]
        points = stats_df2[team2]["points"]
           
            
    col1, col2 = st.columns(2)  # Erstelle zwei Spalten

    

    with col1:  # Linke Spalte für Team 1
            st.write(f"## {team1}")
            st.image(icon_url1, caption=f"Logo: {team1}", width=200)
            st.divider()
            st.write(f"**Anzahl Spiele:** {stats_df1[team1]['matches']}")
            st.write(f"**Anzahl Unentschieden:** {stats_df1[team1]['draws']}")
            st.write(f"**Torverhältnis:** {stats_df1[team1]['goal_difference']}")
            st.write(f"**Punkte:** {stats_df1[team1]['points']}")
            st.write(f"**Anzahl Niederlagen:** {stats_df1[team1]['losses']}")
            st.write(f"**Anzahl Siege:** {stats_df1[team1]['wins']}")
           

    with col2:  # Rechte Spalte für Team 2
            st.write(f"## {team2}")
            st.image(icon_url2, caption=f"Logo: {team2}", width=200)
            st.divider()
            st.write(f"**Anzahl Spiele:** {stats_df2[team2]['matches']}")
            st.write(f"**Anzahl Unentschieden:** {stats_df2[team2]['draws']}")
            st.write(f"**Torverhältnis:** {stats_df2[team2]['goal_difference']}")
            st.write(f"**Punkte:** {stats_df2[team2]['points']}")
            st.write(f"**Anzahl Niederlagen:** {stats_df2[team2]['losses']}")
            st.write(f"**Anzahl Siege:** {stats_df2[team2]['wins']}")


            
            
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
                    st.bar_chart(comp_df["wins"])
        else:
                    st.info("Keine numerischen Kennzahlen zum Vergleich vorhanden.")
            
        with tab2:
                st.subheader("Punkte")
                if not comp_df_display.empty:
                    st.bar_chart(comp_df_display["points"])
                else:
                    st.info("Keine numerischen Kennzahlen zum Vergleich vorhanden.")
            
        with tab3:
            # Letzte 5 Spiele von team1
            team1_games = matches[
            (matches["teams.home.name"] == team1) | (matches["teams.away.name"] == team1)
            ].copy()

# Datum parsen
            team1_games["match_date"] = pd.to_datetime(team1_games["match_date"], errors="coerce")

# Nur die letzten 5 Spiele nach Datum
            team1_last5 = team1_games.sort_values("match_date").tail(5)

# Tore berechnen je nachdem ob Heim oder Auswärts
            team1_last5["goals_scored"] = np.where(
                team1_last5["teams.home.name"] == team1,
                team1_last5["goals.home"],
                team1_last5["goals.away"]
            )

            team1_last5["goals_conceded"] = np.where(
                team1_last5["teams.home.name"] == team1,
                team1_last5["goals.away"],
                team1_last5["goals.home"]
        )

            team1_last5["goal_difference"] = team1_last5["goals_scored"] - team1_last5["goals_conceded"]

# Plot
            st.line_chart(team1_last5.set_index("match_date")["goal_difference"])






            
                

            
            
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

           
    res1 = team_data[team1]
    res2 = team_data[team2]
    col1, col2 = st.columns(2)
    with col1:
            st.subheader(f"{team1} - Heim-Verteilung")
            x = np.arange(6)
            df1 = pd.DataFrame({"Wahrscheinlichkeit": res1["poisson_home"]}, index=x)
            st.bar_chart(df1)
    with col2:
            st.subheader(f"{team2} - Auswärts-Verteilung")
            x = np.arange(6)
            df2 = pd.DataFrame({"Wahrscheinlichkeit": res2["poisson_away"]}, index=x)
            st.bar_chart(df2)
            sm = score_matrix(res1["poisson_home"], res2["poisson_away"])
            fig = plot_score_heatmap(sm, team1, team2)
            st.pyplot(fig)
            o15 = over_under(sm, 1.5)
            o25 = over_under(sm, 2.5)
            o35 = over_under(sm, 3.5)
            st.write(f"Over 1.5: {o15:.2%} | Under 1.5: {(1 - o15):.2%}")
            st.write(f"Over 2.5: {o25:.2%} | Under 2.5: {(1 - o25):.2%}")
            st.write(f"Over 3.5: {o35:.2%} | Under 3.5: {(1 - o35):.2%}")
            idx = int(np.argmax(sm))
            home_goals = idx // sm.shape[1]
            away_goals = idx % sm.shape[1]
            st.write(f"Most probable score: {team1} {home_goals} : {away_goals} {team2} mit {sm[home_goals, away_goals]:.2%}")
                
if __name__ == "__main__":
    main()
