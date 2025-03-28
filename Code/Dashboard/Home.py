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
    st.title("Bundesliga Dashboard")
    
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
    
if __name__ == "__main__":
    main()
