import os
import pandas as pd

from .api_client import ApiSportsClient
from .team_mapping import standardize_team
from .csv_analysis import load_csv_data

def load_fixtures_to_df(api_key, league_id, season, data_dir="data"):
    """
    Lädt die Fixtures von ApiSports (API) und standardisiert die Teamnamen.
    """
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

    if "team_name_std" not in df_csv.columns and "team_title" in df_csv.columns:
        df_csv["team_name_std"] = df_csv["team_title"].apply(standardize_team)
        print("DEBUG: Erzeugte Spalte 'team_name_std' in CSV-Daten.")

    if df_api.empty or df_csv.empty:
        print("Eines der DataFrames ist leer. Merge abgebrochen.")
        return pd.DataFrame()

    merged = df_api.merge(df_csv, left_on="home_team_std", right_on="team_name_std", how="inner")
    return merged

if __name__ == "__main__":
    key = "2cedf059b44f953884d6476e481b8009"
    script_dir = os.path.dirname(__file__)
    csv_file = os.path.join(script_dir, "../../data/filtercsv/filtered_TeamsData.csv")

    print("Ausführen von merge_api_csv:")
    df_merged_api = merge_api_csv(key, 78, 2022, csv_file)
    print("Merged API/CSV shape:", df_merged_api.shape)
    print("Merged API/CSV columns:", df_merged_api.columns)
    print(df_merged_api.head())
