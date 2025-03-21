import streamlit as st
import pandas as pd
from DSKI_Projekt.Code.API.data_processing import run_data_processing_pipeline


# Layout so setzen, dass Streamlit die volle Fensterbreite nutzt:
st.set_page_config(layout="wide", page_title="Bundesliga Dashboard")

def main():
    st.title("Bundesliga Dashboard (Prototyp)")
    
    # Sidebar: Einstellungen
    st.sidebar.header("Einstellungen")
    league = st.sidebar.selectbox("Liga", ["bl1"])  # Nur Bundesliga
    season = st.sidebar.text_input("Saison", "2024")
    use_table = st.sidebar.checkbox("Nur Tabelle anzeigen (OpenLigaDB)", value=True)
    
    # Ansichtsauswahl: Einzelteam oder Teamvergleich
    view_mode = st.sidebar.radio("Ansicht", ("Einzelteam", "Teamvergleich"))
    
    with st.spinner("Verarbeite Daten..."):
        team_data, team_players = run_data_processing_pipeline(use_table=use_table, league=league, season=season)
    
    if not team_data:
        st.warning("Keine verarbeiteten Team-Daten vorhanden.")
        return
    st.success("Aufbereitete Daten erfolgreich geladen!")
    
    # Alle Teams sortiert auflisten
    teams = sorted(team_data.keys())
    
    if view_mode == "Einzelteam":
        # ----------------------
        # EINZELTEAM-ANSICHT
        # ----------------------
        selected_team = st.selectbox("Team auswählen:", teams)
        
        st.subheader(f"Statistiken für {selected_team}")
        stats = team_data[selected_team]["stats"]
        
        # Als DataFrame für eine übersichtliche Darstellung
        stats_df = pd.DataFrame([stats], index=[selected_team]).T
        st.dataframe(stats_df)  # dataFrame statt table -> scrollbar
        
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
    
    else:
        # ----------------------
        # TEAMVERGLEICH
        # ----------------------
        st.subheader("Teamvergleich")
        col1, col2 = st.columns(2)
        with col1:
            team1 = st.selectbox("Team 1 auswählen:", teams, key="team1")
        with col2:
            team2 = st.selectbox("Team 2 auswählen:", teams, key="team2")
        
        if team1 == team2:
            st.error("Bitte zwei unterschiedliche Teams auswählen.")
        else:
            stats1 = team_data[team1]["stats"]
            stats2 = team_data[team2]["stats"]
            comp_df = pd.DataFrame([stats1, stats2], index=[team1, team2])
            
            st.subheader("Vergleichstabelle")
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
            
            # Mit st.dataframe() kannst du scrollen, falls es breiter wird
            st.dataframe(comp_df_display)
            
            st.subheader("Vergleichsdiagramm")
            # Falls du alle (o. g. selektierten) numerischen Spalten plotten willst:
            if not comp_df_display.empty:
                st.bar_chart(comp_df_display.T)
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
