import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from DSKI_Projekt.src.data.data_processing import run_data_processing_pipeline
from DSKI_Projekt.src.analysis.poisson import calc_poisson_for_all_teams

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
    st.set_page_config(layout="wide", page_title="Fußballdashboard")
    st.title("Fußballdashboard: Vergleich und Analyse")
    with st.spinner("Daten werden geladen..."):
        team_data, team_players, df_matches, df_match_data = run_data_processing_pipeline(use_table=False)
    st.sidebar.header("Analyse-Einstellungen")
    mode = st.sidebar.radio("Modus", ["Gemeinsame Analyse", "Einzelanalyse", "Matches", "MatchData", "Poisson 2-Teams"])
    teams = sorted(team_data.keys())
    if mode == "Gemeinsame Analyse":
        st.subheader("Vergleich zweier Teams")
        if not teams:
            st.warning("Keine Teamdaten verfügbar.")
            return
        t1 = st.selectbox("Team 1 auswählen", teams, key="team1")
        t2 = st.selectbox("Team 2 auswählen", teams, key="team2")
        if t1 == t2:
            st.error("Bitte zwei unterschiedliche Teams auswählen!")
            return
        st.write(f"**Team 1**: {t1}, **Team 2**: {t2}")
        m_between = df_matches[((df_matches['home_team_std'] == t1) & (df_matches['away_team_std'] == t2)) | ((df_matches['home_team_std'] == t2) & (df_matches['away_team_std'] == t1))]
        if m_between.empty:
            st.info("Keine direkten Duelle gefunden.")
        else:
            st.dataframe(m_between)
    elif mode == "Einzelanalyse":
        st.subheader("Einzelanalyse eines Teams")
        if not teams:
            st.warning("Keine Teamdaten verfügbar.")
            return
        sel = st.selectbox("Team auswählen", teams)
        st.write(f"**Ausgewähltes Team**: {sel}")
        if sel in team_data:
            stats = team_data[sel]["stats"]
            st.write("### Aggregierte Statistiken")
            st.table(pd.DataFrame([stats]))
            matches = team_data[sel]["matches"]
            if not matches.empty:
                st.write("### Letzte 5 Spiele")
                st.dataframe(matches.tail(5))
            else:
                st.info("Keine Spieldaten für dieses Team.")
        else:
            st.warning("Team nicht in den Daten enthalten.")
        st.write("### Spielerdaten")
        if sel in team_players:
            st.dataframe(team_players[sel])
        else:
            st.info("Keine Spielerdaten gefunden.")
    elif mode == "Matches":
        st.subheader("Alle Matches")
        st.write(f"Anzahl Datensätze: {len(df_matches)}")
        st.dataframe(df_matches.head(20))
    elif mode == "MatchData":
        st.subheader("MatchData")
        st.write(f"Anzahl Datensätze: {len(df_match_data)}")
        st.dataframe(df_match_data.head(20))
    elif mode == "Poisson 2-Teams":
        st.subheader("Poisson-Prognose für zwei Teams")
        data = calc_poisson_for_all_teams(league="bl1", season=2024, max_matchday=34, max_goals=5)
        if not data:
            st.error("Keine Daten für Poisson-Berechnung.")
            return
        team1 = st.selectbox("Team 1 (Heim)", sorted(data.keys()), key="p2team1")
        team2 = st.selectbox("Team 2 (Auswärts)", sorted(data.keys()), key="p2team2")
        if team1 == team2:
            st.error("Bitte zwei unterschiedliche Teams auswählen!")
            return
        res1 = data[team1]
        res2 = data[team2]
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
