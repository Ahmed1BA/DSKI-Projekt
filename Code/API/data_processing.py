import pandas as pd
from merge_data import merge_api_csv

def simple_prediction(home_team, away_team, home_form, away_form):
    if home_form > away_form:
        return f"Win for {home_team}"
    elif home_form < away_form:
        return f"Win for {away_team}"
    return "Draw"

def run_prediction_example():
    home = "bayern münchen"
    away = "borussia dortmund"
    home_form = 0.8
    away_form = 0.7
    result = simple_prediction(home, away, home_form, away_form)
    print("Prediction:", result)

def run_full_pipeline():
    key = "2cedf059b44f953884d6476e481b8009"
    csv_file = "/Users/nicolas/Desktop/Uni/Vorlesungen/2. Semester/Data Science Projekt/DS_Project/filtered/filtered_TeamsData_std.csv"
    df_merged = merge_api_csv(key, 78, 2022, csv_file)
    print("Merged DataFrame shape:", df_merged.shape)

if __name__ == "__main__":
    run_prediction_example()
    run_full_pipeline()
