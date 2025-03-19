import pandas as pd
from api_client import ApiSportsClient
from team_mapping import standardize_team
from csv_analysis import load_csv_data
from openligadb import OpenLigaDBClient

def load_fixtures_to_df(api_key, league_id, season, data_dir="data"):
    client = ApiSportsClient(api_key, data_dir=data_dir)
    data = client.get_fixtures(league_id, season)
    if not data:
        print("DEBUG: Keine Daten von der API erhalten.")
        return pd.DataFrame()
    fixtures = data.get("response", [])
    df = pd.json_normalize(fixtures)
    if "teams.home.name" in df.columns and "teams.away.name" in df.columns:
        df["home_team_std"] = df["teams.home.name"].apply(standardize_team)
        df["away_team_std"] = df["teams.away.name"].apply(standardize_team)
    return df

def merge_api_csv(api_key, league_id, season, csv_path):
    """
    Merge von API-Daten (historische Saison) und CSV-Daten.
    """
    df_api = load_fixtures_to_df(api_key, league_id, season)
    print("DEBUG: API DataFrame shape:", df_api.shape)
    print("DEBUG: API DataFrame head:\n", df_api.head())

    df_csv = load_csv_data(csv_path, team_col="team_title")
    print("DEBUG: CSV DataFrame shape:", df_csv.shape)
    print("DEBUG: CSV DataFrame head:\n", df_csv.head())

    if df_api.empty or df_csv.empty:
        print("Eines der DataFrames ist leer. Merge abgebrochen.")
        return pd.DataFrame()
    merged = df_api.merge(df_csv, left_on="home_team_std", right_on="team_name_std", how="inner")
    return merged

def load_openligadb_matches_to_df(matchdays=range(1, 35), league="bl1", season="2024", data_dir="data/openligadb"):
    """
    Ruft alle Spieltagdaten von OpenLigaDB ab und wandelt sie in ein DataFrame um.
    """
    client = OpenLigaDBClient(league=league, season=season, data_dir=data_dir)
    match_data = client.get_all_matchdays(matchdays)
    if not match_data:
        print("DEBUG: Keine Daten von OpenLigaDB erhalten.")
        return pd.DataFrame()
    df = client.matches_to_df(match_data)
    return df

def merge_openligadb_csv(csv_path, matchdays=range(1, 35), league="bl1", season="2024", data_dir="data/openligadb"):
    """
    Merge von aktuellen OpenLigaDB-Daten und den historischen CSV-Daten.
    """
    df_openliga = load_openligadb_matches_to_df(matchdays, league, season, data_dir)
    print("DEBUG: OpenLigaDB DataFrame shape:", df_openliga.shape)
    print("DEBUG: OpenLigaDB DataFrame head:\n", df_openliga.head())
    
    if "home_team_std" not in df_openliga.columns:
        for col in ["home_team", "teams.home.name", "team_h"]:
            if col in df_openliga.columns:
                print(f"DEBUG: Verwende Spalte '{col}' zur Standardisierung der Heimteams.")
                df_openliga["home_team_std"] = df_openliga[col].apply(standardize_team)
                break
        if "home_team_std" not in df_openliga.columns:
            print("WARNUNG: Keine geeignete Spalte für Home Team in OpenLigaDB Daten gefunden. Merge abgebrochen.")
            return pd.DataFrame()

    df_csv = load_csv_data(csv_path, team_col="team_title")
    print("DEBUG: CSV DataFrame shape:", df_csv.shape)
    print("DEBUG: CSV DataFrame head:\n", df_csv.head())

    if df_openliga.empty or df_csv.empty:
        print("Eines der DataFrames ist leer. Merge abgebrochen.")
        return pd.DataFrame()
    merged = df_openliga.merge(df_csv, left_on="home_team_std", right_on="team_name_std", how="inner")
    return merged

if __name__ == "__main__":
    key = "2cedf059b44f953884d6476e481b8009"
    csv_file = "/Users/nicolas/Desktop/Uni/Vorlesungen/2. Semester/Data Science Projekt/DS_Project/filtered/filtered_TeamsData.csv"

    print("Ausführen von merge_api_csv:")
    df_merged_api = merge_api_csv(key, 78, 2022, csv_file)
    print("Merged API/CSV shape:", df_merged_api.shape)
    print("Merged API/CSV columns:", df_merged_api.columns)

    print("\nAusführen von merge_openligadb_csv:")
    df_merged_openliga = merge_openligadb_csv(csv_file, matchdays=range(1, 35), league="bl1", season="2024", data_dir="data/openligadb")
    print("Merged OpenLigaDB/CSV shape:", df_merged_openliga.shape)
    print("Merged OpenLigaDB/CSV columns:", df_merged_openliga.columns)
