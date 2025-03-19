import pandas as pd
import os
from Code.API.team_mapping import standardize_team

def load_csv_data(csv_path, team_col=None):
    """
    Lädt eine CSV-Datei und, falls team_col angegeben wird und existiert,
    standardisiert die Teamnamen und fügt die Spalte 'team_name_std' hinzu.
    """
    print(f"DEBUG: Versuche CSV zu laden: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"DEBUG: Datei existiert nicht: {csv_path}")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print("Fehler beim Einlesen der CSV-Datei:", e)
        return pd.DataFrame()
    
    print(f"DEBUG: CSV erfolgreich geladen, Shape: {df.shape}")
    print("DEBUG: Spalten:", df.columns.tolist())
    
    if team_col is not None and team_col in df.columns:
        print(f"DEBUG: Standardisiere Teamnamen in Spalte '{team_col}'.")
        df["team_name_std"] = df[team_col].apply(standardize_team)
    elif team_col is not None:
        print(f"WARNUNG: Spalte '{team_col}' nicht gefunden. Keine Standardisierung.")
    
    return df

def load_all_filtered_csvs(base_path):
    """
    Liest alle vier gefilterten CSV-Dateien aus dem angegebenen Ordner ein.
    Erwartete Dateien:
      - filtered_MatchData.csv
      - filtered_TeamsData.csv
      - filtered_PlayersData_perYear.csv
      - filtered_Matches.csv
    """
    match_data_path   = os.path.join(base_path, "filtered_MatchData.csv")
    teams_data_path   = os.path.join(base_path, "filtered_TeamsData.csv")
    players_data_path = os.path.join(base_path, "filtered_PlayersData_perYear.csv")
    matches_path      = os.path.join(base_path, "filtered_Matches.csv")
    
    df_match_data   = load_csv_data(match_data_path, team_col=None)
    df_teams_data   = load_csv_data(teams_data_path, team_col="team_title")
    df_players_data = load_csv_data(players_data_path, team_col=None)
    df_matches      = load_csv_data(matches_path, team_col=None)

    print("\n=== Zusammenfassung aller geladenen DataFrames ===")
    print("MatchData Shape:",   df_match_data.shape)
    print("TeamsData Shape:",   df_teams_data.shape)
    print("PlayersData Shape:", df_players_data.shape)
    print("Matches Shape:",     df_matches.shape)
    
    return df_match_data, df_teams_data, df_players_data, df_matches

def analyze_csv_data(df, label="DataFrame"):
    """
    Gibt grundlegende Informationen zu einem DataFrame aus.
    """
    if df.empty:
        print(f"{label} ist leer oder konnte nicht geladen werden.")
        return
    
    print(f"\n=== Analyse: {label} ===")
    print("Shape:", df.shape)
    print("Spalten:", df.columns.tolist())
    print(df.head())

if __name__ == "__main__":
    base_path = "/Users/nicolas/Desktop/Uni/Vorlesungen/2. Semester/Data Science Projekt/DS_Project/filtered"
    
    df_match_data, df_teams_data, df_players_data, df_matches = load_all_filtered_csvs(base_path)
    
    analyze_csv_data(df_match_data,   label="MatchData")
    analyze_csv_data(df_teams_data,   label="TeamsData")
    analyze_csv_data(df_players_data, label="PlayersData")
    analyze_csv_data(df_matches,      label="Matches")
