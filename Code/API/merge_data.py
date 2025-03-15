import pandas as pd
from api_client import ApiSportsClient
from team_mapping import standardize_team
from csv_analysis import load_csv_data

def load_fixtures_to_df(api_key, league_id, season, data_dir="data"):
    client = ApiSportsClient(api_key, data_dir=data_dir)
    data = client.get_fixtures(league_id, season)
    if not data:
        return pd.DataFrame()
    fixtures = data.get("response", [])
    df = pd.json_normalize(fixtures)
    if "teams.home.name" in df.columns and "teams.away.name" in df.columns:
        df["home_team_std"] = df["teams.home.name"].apply(standardize_team)
        df["away_team_std"] = df["teams.away.name"].apply(standardize_team)
    return df

def merge_api_csv(api_key, league_id, season, csv_path):
    df_api = load_fixtures_to_df(api_key, league_id, season)
    df_csv = load_csv_data(csv_path, team_col="team_title")
    if df_api.empty or df_csv.empty:
        print("One of the DataFrames is empty, merge aborted.")
        return pd.DataFrame()
    merged = df_api.merge(df_csv, left_on="home_team_std", right_on="team_name_std", how="inner")
    return merged

if __name__ == "__main__":
    key = "2cedf059b44f953884d6476e481b8009"
    csv_file = "/Users/nicolas/Desktop/Uni/Vorlesungen/2. Semester/Data Science Projekt/DS_Project/filtered/filtered_TeamsData_std.csv"
    df_merged = merge_api_csv(key, 78, 2022, csv_file)
    print("Merged shape:", df_merged.shape)
    print("Merged columns:", df_merged.columns)
