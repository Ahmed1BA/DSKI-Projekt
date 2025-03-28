import streamlit as st
import pandas as pd

from DSKI_Projekt.Code.API.data_processing import run_data_processing_pipeline

def main():
    st.set_page_config(layout="wide", page_title="Fußballdashboard")
    st.title("Fußballdashboard: Vergleich und Analyse")
    
    with st.spinner("Daten werden geladen..."):
        team_data, team_players, df_matches, df_match_data = run_data_processing_pipeline(use_table=False)

    st.sidebar.header("Analyse-Einstellungen")
    mode = st.sidebar.radio("Modus", ["Gemeinsame Analyse", "Einzelanalyse", "Matches", "MatchData"])
    
    teams = sorted(team_data.keys())

    if mode == "Gemeinsame Analyse":
        st.subheader("Vergleich zweier Teams")
        if not teams:
            st.warning("Keine Teamdaten verfügbar.")
            return
        team1 = st.selectbox("Team 1 auswählen", teams, key="team1")
        team2 = st.selectbox("Team 2 auswählen", teams, key="team2")
        if team1 == team2:
            st.error("Bitte zwei unterschiedliche Teams auswählen!")
            return
        
        st.write(f"**Team 1**: {team1}, **Team 2**: {team2}")
        matches_between = df_matches[
            ((df_matches['home_team_std'] == team1) & (df_matches['away_team_std'] == team2)) |
            ((df_matches['home_team_std'] == team2) & (df_matches['away_team_std'] == team1))
        ]
        if matches_between.empty:
            st.info("Keine direkten Duelle in df_matches gefunden.")
        else:
            st.dataframe(matches_between)

    elif mode == "Einzelanalyse":
        st.subheader("Einzelanalyse eines Teams")
        if not teams:
            st.warning("Keine Teamdaten verfügbar.")
            return
        selected_team = st.selectbox("Team auswählen", teams)
        st.write(f"**Ausgewähltes Team**: {selected_team}")
        
        if selected_team in team_data:
            stats = team_data[selected_team]["stats"]
            st.write("### Aggregierte Statistiken")
            st.table(pd.DataFrame([stats]))

            matches = team_data[selected_team]["matches"]
            if not matches.empty:
                st.write("### Letzte 5 Spiele")
                st.dataframe(matches.tail(5))
            else:
                st.info("Keine Spieldaten für dieses Team.")
        else:
            st.warning("Team nicht in den Daten enthalten.")
        
        st.write("### Spielerdaten")
        if selected_team in team_players:
            st.dataframe(team_players[selected_team])
        else:
            st.info("Keine Spielerdaten für dieses Team gefunden.")

    elif mode == "Matches":
        st.subheader("Alle Matches (filtered_Matches.csv)")
        st.write(f"Anzahl Datensätze: {len(df_matches)}")
        st.dataframe(df_matches.head(20)) 

    else: 
        st.subheader("MatchData (filtered_MatchData.csv)")
        st.write(f"Anzahl Datensätze: {len(df_match_data)}")
        st.dataframe(df_match_data.head(20)) 

if __name__ == "__main__":
    main()
