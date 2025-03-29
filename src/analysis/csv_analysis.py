import pandas as pd
import os
import logging

from ..mapping.team_mapping import standardize_team

def load_csv_data(csv_path, team_col=None):
    if not os.path.exists(csv_path):
        logging.warning("Datei existiert nicht: %s", csv_path)
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(csv_path)
        logging.info("CSV geladen: %s (Shape: %s)", csv_path, df.shape)
    except Exception as e:
        logging.error("Fehler beim Einlesen der CSV-Datei %s: %s", csv_path, e)
        return pd.DataFrame()
    
    if team_col is not None and team_col in df.columns:
        logging.info("Standardisiere Teamnamen in Spalte '%s'.", team_col)
        df["team_name_std"] = df[team_col].apply(standardize_team)
    elif team_col is not None:
        logging.warning("Spalte '%s' nicht gefunden. Keine Standardisierung.", team_col)
    
    return df

def load_all_filtered_csvs(base_path):
    files = {
        "match_data":   ("filtered_MatchData.csv", None),
        "teams_data":   ("filtered_TeamsData.csv", "team_title"),
        "players_data": ("filtered_PlayersData_perYear.csv", None),
        "matches":      ("filtered_Matches.csv", None)
    }

    dfs = {}
    for key, (filename, team_col) in files.items():
        path = os.path.join(base_path, filename)
        dfs[key] = load_csv_data(path, team_col)

    for key, df in dfs.items():
        logging.info("Geladen: %-15s → %s Zeilen", key, df.shape[0])

    return dfs["match_data"], dfs["teams_data"], dfs["players_data"], dfs["matches"]

def analyze_csv_data(df, label="DataFrame"):
    if df.empty:
        logging.warning("%s ist leer oder konnte nicht geladen werden.", label)
        return
    logging.info("=== Analyse: %s ===", label)
    logging.info("Shape: %s", df.shape)
    logging.info("Spalten: %s", df.columns.tolist())
    logging.debug("\n%s", df.head())

if __name__ == "__main__":
    from ..logging_config import setup_logging
    setup_logging("logs/csv_analysis.log")

    script_dir = os.path.dirname(__file__)
    base_path = os.path.join(script_dir, "../../data/filtercsv")

    df_match_data, df_teams_data, df_players_data, df_matches = load_all_filtered_csvs(base_path)

    analyze_csv_data(df_match_data,   label="MatchData")
    analyze_csv_data(df_teams_data,   label="TeamsData")
    analyze_csv_data(df_players_data, label="PlayersData")
    analyze_csv_data(df_matches,      label="Matches")
