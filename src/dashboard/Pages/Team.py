import streamlit as st
import pandas as pd


from src.data.data_processing import run_data_processing_pipeline
from src.analysis.poisson import calc_poisson_for_all_teams


st.set_page_config(layout="wide", page_title="Einzelanalyse")

def main():

    st.image("src/dashboard/pages/logo.png", width=100, use_container_width=False) 
    st.title("Football Dashboard")

    st.subheader("Einzelanalyse für ein Team")
    
    st.sidebar.header("Einstellungen")
    league = "bl1"
    season = st.sidebar.text_input("Saison", "2024")
    use_table = True
    
    with st.spinner("Verarbeite Daten..."):
        team_data, team_players, df_matches, df_match_data = run_data_processing_pipeline(use_table=use_table, league=league, season=season)

    
    if not team_data:
        st.warning("Keine verarbeiteten Team-Daten vorhanden. --> Hilfe findest du in der README")
        return
    st.success("Aufbereitete Daten erfolgreich geladen!")
    
    teams = sorted(team_data.keys())
    selected_team = st.selectbox("Team auswählen:", teams)
        
    st.subheader(f"{selected_team}")
    stats = team_data[selected_team]["stats"]
        
    stats_df = pd.DataFrame([stats], index=[selected_team]).T
    
    icon_url = stats_df[selected_team]["teamIconUrl"]
    wins = stats_df[selected_team]["won"]
    lost = stats_df[selected_team]["lost"]
    draw = stats_df[selected_team]["draw"]
    goalDifference = stats_df[selected_team]["goalDiff"]
    goals = stats_df[selected_team]["goals"]
    goalsAgainst = stats_df[selected_team]["opponentGoals"]
    points = stats_df[selected_team]["points"]
    st.write("### Statistiken aus der aktuellen Saison")
    st.write(f"Anzahl Spiele: {stats_df[selected_team]['matches']}")
    st.write(f"Anzahl Unentschieden: {draw}")
    st.write(f"Torverhältnis: {goals} : {goalsAgainst} ({goalDifference})")
    st.write(f"Punkte: {points}")
    st.write(f"Anzahl Niederlagen: {lost}")
    st.write(f"Anzahl Siege: {wins}")
    st.image(icon_url, caption=f"Logo: {selected_team}",width=200)
    #Spielerdaten
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

    def show_team_players(team_name):
        
            st.markdown(f"### Spielerdaten für **{team_name}**")
            if team_name in team_players:
                excluded_columns = ["id", "team_title", "team_name_std", "league", "time"]
                df = team_players[team_name].drop(columns=excluded_columns, errors='ignore')
                styled_df = style_dataframe_top_bottom(df)
                st.dataframe(styled_df, use_container_width=True)
            else:
                st.info(f"Keine Spielerdaten für **{team_name}** gefunden.")

    show_team_players(selected_team)
    with st.expander("ℹ️ Farblegende"):
            st.markdown("""
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="width: 100px; height: 20px; background: #fee08b;"></div> 🟡 Besonders schwach<br>
                <div style="width: 100px; height: 20px; background: #1a9850;"></div> 🟢 Starker Wert
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

