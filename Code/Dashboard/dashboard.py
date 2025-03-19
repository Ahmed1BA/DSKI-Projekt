import streamlit as st
from Code.API.merge_data import merge_api_csv, merge_openligadb_csv


def main():
    st.title("Bundesliga Dashboard (Prototyp)")

    st.sidebar.title("Einstellungen")
    # Trage hier deinen tatsächlichen API-Key ein oder lass das Feld zum Testen leer
    api_key = st.sidebar.text_input("API-Key", value="DEIN_API_KEY_HIER")
    
    # Passe den Pfad zur CSV-Datei an deine lokale Struktur an
    csv_file = st.sidebar.text_input(
        "Pfad zur CSV-Datei",
        value="/Users/nicolas/Desktop/Uni/Vorlesungen/2. Semester/Data Science Projekt/DS_Project/filtered/filtered_TeamsData.csv"
    )

    # Auswahl: API-Daten oder OpenLigaDB-Daten
    data_source = st.sidebar.selectbox("Datenquelle wählen", ["API + CSV", "OpenLigaDB + CSV"])

    if st.sidebar.button("Daten laden"):
        with st.spinner("Lade und merge Daten..."):
            if data_source == "API + CSV":
                # Beispiel: Bundesliga 2022 (league_id=78)
                df_merged = merge_api_csv(api_key, league_id=78, season=2022, csv_path=csv_file)
            else:
                # Beispiel: BL1, Saison 2024, alle Spieltage (1 bis 34)
                df_merged = merge_openligadb_csv(
                    csv_file,
                    matchdays=range(1, 35),
                    league="bl1",
                    season="2024",
                    data_dir="data/openligadb"
                )
        
        if df_merged.empty:
            st.warning("Der gemergte DataFrame ist leer. Bitte überprüfe die Datenquelle oder den Pfad.")
        else:
            st.success(f"Erfolgreich Daten geladen! Shape: {df_merged.shape}")

            # Kurze Vorschau der Daten
            st.subheader("Vorschau der Daten")
            st.dataframe(df_merged.head(10))

            # Team-Auswahl für einfache Visualisierung
            st.subheader("Team-Auswahl")
            if "home_team_std" in df_merged.columns:
                teams = sorted(df_merged["home_team_std"].dropna().unique())
                selected_team = st.selectbox("Team auswählen:", teams)
                
                # Daten für das ausgewählte Team filtern
                team_data = df_merged[df_merged["home_team_std"] == selected_team]
                st.write(f"Anzahl Spiele für **{selected_team}**:", len(team_data))

                # Beispiel: Liniendiagramm der 'goals.home' (falls vorhanden)
                if "goals.home" in team_data.columns:
                    st.line_chart(team_data["goals.home"], height=300)
                else:
                    st.info("Keine Spalte 'goals.home' im DataFrame gefunden.")
            else:
                st.info("Keine Spalte 'home_team_std' im DataFrame. Evtl. falsche Datenquelle?")
    else:
        st.info("Bitte Datenquelle und CSV-Pfad eingeben und auf 'Daten laden' klicken.")

if __name__ == "__main__":
    main()
