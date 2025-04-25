import streamlit as st
import pandas as pd


from src.data.data_processing import run_data_processing_pipeline
from src.analysis.poisson import calc_poisson_for_all_teams
from src.api.openligadb_table import get_current_bundesliga_table


st.set_page_config(layout="wide", page_title="Tabelle")

def main():

    st.image("src/dashboard/pages/logo.png", width=100, use_container_width=False) 
    st.title("Football Dashboard")

    st.sidebar.header("Einstellungen")
    league = "bl1"
    season = st.sidebar.text_input("Saison", "2024")

    df_table = get_current_bundesliga_table(league=league, season=season)
    if df_table is None:
        st.warning("Keine Tabelle gefunden. --> Hilfe findest du in der README")
        return
    st.success("Tabelle erfolgreich geladen!")
    st.write("### Tabelle")

    # Apply light blue background to the first 4 rows
    def champion_leauge(row):
        if row.name < 4:  # Check if the row index is less than 4
            return ['background-color: lightblue'] * len(row)
        return [''] * len(row)
    
    
    # Apply light blue background to the first 4 rows
    df_table = df_table.rename(columns={
        "teamName": "Mannschaft",
        "points": "Punkte",
        "won": "Siege",
        "draw": "Unentschieden",
        "lost": "Niederlagen",
        "goals": "Tore ",
        "opponentGoals": "Gegentore",
        "goalDiff": "Tordifferenz",
        "matches": "Spiele",
    })

    def euro_league(row):
        if row.name == 4:  # 5th place (index 4)
            return ['background-color: #FFD69D'] * len(row)
        return [''] * len(row)
    
    def conference_league(row):
        if row.name == 5:
            return ['background-color: lightgreen'] * len(row)
        return [''] * len(row)


    def relegation_zone(row):
        if row.name == 15:  # 16th place (index 16)
            return ['background-color: lightcoral'] * len(row)
        elif row.name >= 16:  # 17th and 18th place (index 17 and 18)
            return ['background-color: red'] * len(row)
        return [''] * len(row)

    df_table = df_table.drop(columns=["teamInfoId", "shortName", "teamIconUrl"], errors="ignore")
    styled_table = df_table.style.apply(champion_leauge, axis=1).apply(euro_league, axis=1).apply(conference_league, axis=1).apply(relegation_zone, axis=1)
    st.dataframe(styled_table, use_container_width=True)

    with st.expander("ℹ️ Farblegende"):
            st.markdown("""
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="width: 100px; height: 20px; background: lightblue;"></div> Champions Leauge <br>
                <div style="width: 100px; height: 20px; background: #FFD69D;"></div> Europa Leauge <br>
                <div style="width: 100px; height: 20px; background: lightgreen;"></div> Conference Leauge <br>
                <div style="width: 100px; height: 20px; background: red;"></div> Abstieg <br>
                <div style="width: 100px; height: 20px; background: lightcoral;"></div> Relegation <br>
                
            </div>
            """, unsafe_allow_html=True)
    

if __name__ == "__main__":
    main()

