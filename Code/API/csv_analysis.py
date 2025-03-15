import pandas as pd
import os
from team_mapping import standardize_team

def load_csv_data(csv_path, team_col="team_title"):
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    if team_col in df.columns:
        df["team_name_std"] = df[team_col].apply(standardize_team)
    return df

def analyze_csv_data(csv_path, team_col="team_title"):
    df = load_csv_data(csv_path, team_col)
    if df.empty:
        print("No data found or file not found:", csv_path)
        return
    print("Number of rows:", len(df))
    print("Unique teams:", df["team_name_std"].unique())

if __name__ == "__main__":
    sample_csv = "/Users/nicolas/Desktop/Uni/Vorlesungen/2. Semester/Data Science Projekt/DS_Project/filtered/filtered_TeamsData_std.csv"
    analyze_csv_data(sample_csv, team_col="team_title")
