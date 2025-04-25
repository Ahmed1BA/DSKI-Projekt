import streamlit as st
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

from src.data.data_processing import run_data_processing_pipeline
from src.analysis.poisson import calc_poisson_for_all_teams  
import matplotlib.colors as mcolors


st.set_page_config(layout="wide", page_title="Team Vergleich")
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
    st.image("src/dashboard/pages/logo.png", width=100, use_container_width=False)
    st.title("Football Dashboard")
    
    st.sidebar.header("Einstellungen")
    league = "bl1"
    season = st.sidebar.text_input("Saison", "2024")
    use_table = True
    
    
        
    with st.spinner("Verarbeite Daten..."):
        team_data, team_players, df_matches, _ = run_data_processing_pipeline(use_table=False)

    if not team_data:
        st.warning("Keine verarbeiteten Team-Daten vorhanden. --> Hilfe findest du in der README")
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
            st.subheader("Direkte Duelle")
            excluded_columns = ["id", "fid", "league_id", "season", "h", "a", "home_team_std", "away_team_std"]
            st.dataframe(m_between.drop(columns=excluded_columns, errors='ignore'))
        stats1 = team_data[team1]["stats"]
        stats2 = team_data[team2]["stats"]
        comp_df = pd.DataFrame([stats1, stats2], index=[team1, team2])
             
        stats_df1 = pd.DataFrame([stats1], index=[team1]).T
        stats_df2 = pd.DataFrame([stats2], index=[team2]).T
        matches = team_data[team1]["matches"]
        matches2 = team_data[team2]["matches"]

        wins = stats_df1[team1]["wins"]
        lost = stats_df1[team1]["losses"]
        draw = stats_df1[team1]["draws"]
        goalDifference = stats_df1[team1]["goal_difference"]
        goals = stats_df1[team1]["goals_scored"]
        goalsAgainst = stats_df1[team1]["goals_conceded"]
        points = stats_df1[team1]["points"]
           

        icon_url1 = matches.iloc[0]["teams.home.logo"] if matches.iloc[0]["teams.home.name"] == team1 else matches.iloc[0]["teams.away.logo"]
        icon_url2 = matches2.iloc[0]["teams.home.logo"] if matches2.iloc[0]["teams.home.name"] == team2 else matches2.iloc[0]["teams.away.logo"]
            
        # Statistiken für Team 2
        wins = stats_df2[team2]["wins"]
        lost = stats_df2[team2]["losses"]
        draw = stats_df2[team2]["draws"]
        goalDifference = stats_df2[team2]["goal_difference"]
        goals = stats_df2[team2]["goals_scored"]
        goalsAgainst = stats_df2[team2]["goals_conceded"]
        points = stats_df2[team2]["points"]
           
            
    col1, col2 = st.columns(2)  

    

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


            
            
           
            columns_of_interest = [
                "matches", "wins", "draws", "losses",
                "goals_scored", "goals_conceded", "goal_difference", "points",
                # xG-Metriken:
                "avg_xG", "avg_xGA", "avg_npxG", "avg_npxGA",
                "avg_ppda_att", "avg_ppda_def"
            ]
            available_cols = [c for c in columns_of_interest if c in comp_df.columns]
            comp_df_display = comp_df[available_cols]
            
            
    st.title("Vergleich der Teams")
    st.write("Hier kannst du die Teams vergleichen.")
    tab1, tab2, tab3, tab4 = st.tabs(["Siege", "Punkte", "Possession-Analyse", "Spielerdaten"])
            
    with tab1:
        st.subheader("Siege")
                
           
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
        st.subheader("Poisson-Prognose für zwei Teams")
        data = calc_poisson_for_all_teams(league="bl1", season=2024, max_matchday=34, max_goals=5)
        if not data:
            st.error("Keine Daten für Poisson-Berechnung.")
        res1 = data[team1]
        res2 = data[team2]
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{team1} - Heim-Verteilung")
            x = np.arange(6)
            df1 = pd.DataFrame({"Tore": x, "Wahrscheinlichkeit": res1["poisson_home"]})
            fig1 = px.bar(df1, x="Tore", y="Wahrscheinlichkeit",
                      labels={"Tore": "Tore", "Wahrscheinlichkeit": "Wahrscheinlichkeit"},
                      title="")
            fig1.update_layout(xaxis_title="Tore", yaxis_title="Wahrscheinlichkeit")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.subheader(f"{team2} - Auswärts-Verteilung")
            x = np.arange(6)
            df2 = pd.DataFrame({"Tore": x, "Wahrscheinlichkeit": res2["poisson_away"]})
            fig2 = px.bar(df2, x="Tore", y="Wahrscheinlichkeit",
                          labels={"Tore": "Tore", "Wahrscheinlichkeit": "Wahrscheinlichkeit"},
                            title="")
            fig2.update_layout(xaxis_title="Tore", yaxis_title="Wahrscheinlichkeit")
            st.plotly_chart(fig2, use_container_width=True)

        sm = score_matrix(res1["poisson_home"], res2["poisson_away"])
        o15 = over_under(sm, 1.5)
        o25 = over_under(sm, 2.5)
        o35 = over_under(sm, 3.5)
        idx = int(np.argmax(sm))
        home_goals = idx // sm.shape[1]
        away_goals = idx % sm.shape[1]
        st.write(f"Wahrscheinlichstes Ergebnis: {team1} {home_goals} : {away_goals} {team2} mit {sm[home_goals, away_goals]:.2%}")





            
                

            
            
          
    with tab4:
        st.subheader("Spielerdaten Vergleich")

        col1, col2 = st.columns(2)

        def style_dataframe_top_bottom(df):
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if 'year' in numeric_cols:
                numeric_cols.remove('year')
            styled = df.style.format(precision=2)\
                .set_properties(**{"text-align": "center", "font-size": "14px"})\
                .set_table_styles([
                    {"selector": "thead th", "props": [
                        ("background-color", "#f9f9f9"),
                        ("font-weight", "bold")
                    ]}
                ])
            for col in numeric_cols:
                top_5 = df[col].nlargest(5)
                bottom_5 = df[col].nsmallest(5)
                styled = styled.apply(lambda row, top_5=top_5: ['background-color: green' if val in top_5.values else '' for val in row], subset=[col], axis=1)
                styled = styled.apply(lambda row, bottom_5=bottom_5: ['background-color: yellow' if val in bottom_5.values else '' for val in row], subset=[col], axis=1)
            return styled

        def show_team_players(col, team_name):
            with col:
                st.markdown(f"### Spielerdaten für **{team_name}**")
                if team_name in team_players:
                    excluded_columns = ["id", "team_title", "team_name_std", "league", "time"]
                    df = team_players[team_name].drop(columns=excluded_columns, errors='ignore')
                    styled_df = style_dataframe_top_bottom(df)
                    st.dataframe(styled_df, use_container_width=True)
                else:
                    st.info(f"Keine Spielerdaten für **{team_name}** gefunden.")

        show_team_players(col1, team1)
        show_team_players(col2, team2)

        with st.expander("ℹ️ Farblegende"):
            st.markdown("""
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="width: 100px; height: 20px; background: #fee08b;"></div> 🟡 Besonders schwach<br>
                <div style="width: 100px; height: 20px; background: #1a9850;"></div> 🟢 Starker Wert
            </div>
            """, unsafe_allow_html=True)


    
    
   
            
if __name__ == "__main__":
    main()
