import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.data.data_processing import run_data_processing_pipeline
from src.analysis.poisson import calc_poisson_for_all_teams

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
    st.set_page_config(layout="wide", page_title="Poisson-Analyse")
    st.title("Football Dashboard")
    st.image("src/dashboard/pages/logo.png", width=100, use_container_width=False)
    st.title("Poisson-Analyse für zwei Teams")
    with st.spinner("Daten werden geladen..."):
        team_data, team_players, df_matches, df_match_data = run_data_processing_pipeline(use_table=False)
    
        
        
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
        st.subheader("Ergebnis-Matrix")
        sm = score_matrix(res1["poisson_home"], res2["poisson_away"])
        fig = plot_score_heatmap(sm, team1, team2)
        st.pyplot(fig)
        with st.expander("ℹ️ Farblegende"):
            st.markdown("""
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="width: 100px; height: 20px; background: ;"></div> X und Y Achse geben die jweilige Toranzahl an.<br>
                <div style="width: 100px; height: 20px; background: #101047;"></div> Dunkelblau = hohe Wahrscheinlichkeit<br>
                <div style="width: 100px; height: 20px; background: #f0f0f0;"></div> Hellgrau = niedrige Wahrscheinlichkeit<br>
            </div>
            """, unsafe_allow_html=True)
        st.subheader("Über/Unter-Wahrscheinlichkeiten")
        o15 = over_under(sm, 1.5)
        o25 = over_under(sm, 2.5)
        o35 = over_under(sm, 3.5)
        st.write(f"Über 1.5: {o15:.2%} | Unter 1.5: {(1 - o15):.2%}")
        st.write(f"Über 2.5: {o25:.2%} | Unter 2.5: {(1 - o25):.2%}")
        st.write(f"Über 3.5: {o35:.2%} | Unter 3.5: {(1 - o35):.2%}")
        idx = int(np.argmax(sm))
        home_goals = idx // sm.shape[1]
        away_goals = idx % sm.shape[1]
        st.write(f"Wahrscheinlichstes Ergebnis: {team1} {home_goals} : {away_goals} {team2} mit {sm[home_goals, away_goals]:.2%}")


if __name__ == "__main__":
    main()
