import streamlit as st
import pandas as pd
from data_processing import run_data_processing_pipeline

def main():
    st.title("Bundesliga Dashboard (Prototyp)")
    
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
    
    teams = sorted(team_data.keys())
    selected_team = st.selectbox("Team auswählen:", teams)
    
    st.subheader(f"Statistiken für {selected_team}")
    stats = team_data[selected_team]["stats"]
    st.table(pd.DataFrame([stats]))
    
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
