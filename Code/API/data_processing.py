import os
import pandas as pd

from .merge_data import merge_api_csv
from .openligadb_table import get_current_bundesliga_table
from .team_mapping import standardize_team

def unify_goal_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vereinheitlicht die Tore-Spalten in 'goals.home' und 'goals.away', falls möglich.
    Falls die Tore als Strings vorliegen, werden sie in numerische Werte umgewandelt.
    """
    print("\nDEBUG unify_goal_columns: columns before rename:", df.columns.tolist())
    
    if "goals.home" in df.columns and "goals.away" in df.columns:
        print("DEBUG: 'goals.home'/'goals.away' sind bereits vorhanden.")
    elif "score.fulltime.home" in df.columns and "score.fulltime.away" in df.columns:
        print("DEBUG: Benenne 'score.fulltime.home'/'score.fulltime.away' um in 'goals.home'/'goals.away'.")
        df.rename(columns={
            "score.fulltime.home": "goals.home",
            "score.fulltime.away": "goals.away"
        }, inplace=True)
    else:
        print("WARNUNG: Keine bekannten Tore-Spalten gefunden (goals.home / score.fulltime.home).")

    if "goals.home" in df.columns:
        df["goals.home"] = pd.to_numeric(df["goals.home"], errors="coerce")
    if "goals.away" in df.columns:
        df["goals.away"] = pd.to_numeric(df["goals.away"], errors="coerce")
        
    print("DEBUG unify_goal_columns: columns after rename:", df.columns.tolist(), "\n")
    return df


def prepare_team_data(df: pd.DataFrame) -> dict:
    """
    Aggregiert die Spielstatistiken für jedes Team aus dem gemergten DataFrame (API + Teams-CSV).
    Nutzt:
      - 'home_team_std' / 'away_team_std' für die Teamzuordnung
      - 'goals.home' / 'goals.away' für die Tore
      - ggf. Metriken wie xG, xGA, etc.
    Zusätzlich werden Tordifferenz und Punkte (3 pro Sieg, 1 pro Unentschieden) berechnet.
    """
    teams = set(df['home_team_std']).union(set(df['away_team_std']))
    
    metrics = [
        'xG', 'xGA', 'npxG', 'npxGA', 'ppda_att', 'ppda_def',
        'ppda_allowed_att', 'ppda_allowed_def', 'deep', 'deep_allowed',
        'scored', 'missed', 'xpts', 'npxGD'
    ]
    metrics = [m for m in metrics if m in df.columns]
    
    team_data = {}
    for team in teams:
        team_matches = df[(df['home_team_std'] == team) | (df['away_team_std'] == team)]
        
        wins = draws = losses = 0
        goals_scored = goals_conceded = 0
        metric_sums = {m: 0.0 for m in metrics}
        
        for _, row in team_matches.iterrows():
            if row['home_team_std'] == team:
                home_goals = row.get('goals.home', 0)
                away_goals = row.get('goals.away', 0)
                goals_scored += home_goals
                goals_conceded += away_goals
                if home_goals > away_goals:
                    wins += 1
                elif home_goals == away_goals:
                    draws += 1
                else:
                    losses += 1
                for m in metrics:
                    metric_sums[m] += row[m]
            else:
                home_goals = row.get('goals.home', 0)
                away_goals = row.get('goals.away', 0)
                goals_scored += away_goals
                goals_conceded += home_goals
                if away_goals > home_goals:
                    wins += 1
                elif away_goals == home_goals:
                    draws += 1
                else:
                    losses += 1
                for m in metrics:
                    metric_sums[m] += row[m]
        
        num_matches = len(team_matches)
        averages = {
            f"avg_{m}": (metric_sums[m] / num_matches) if num_matches > 0 else None
            for m in metric_sums
        }
        
        stats = {
            'matches': num_matches,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded,
            'goal_difference': goals_scored - goals_conceded,
            'points': wins * 3 + draws
        }
        stats.update(averages)
        
        team_data[team] = {
            'matches': team_matches,
            'stats': stats
        }
    
    return team_data


def prepare_player_data(players_df: pd.DataFrame) -> dict:
    """
    Gruppiert die Spielerdaten nach 'team_name_std' (falls vorhanden),
    sonst nach 'team_title'.
    """
    team_players = {}
    if "team_name_std" in players_df.columns:
        for team, group in players_df.groupby("team_name_std"):
            team_players[team] = group.reset_index(drop=True)
    else:
        for team, group in players_df.groupby("team_title"):
            team_players[team] = group.reset_index(drop=True)
    return team_players


def prepare_filtered_matches(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardisiert das CSV 'filtered_Matches':
      - 'team_h' => 'home_team_std', 'team_a' => 'away_team_std'
      - Spalten, die mit 'h_' oder 'a_' beginnen, werden umbenannt in 'home_*' / 'away_*'
      - 'home_goals' / 'away_goals' => 'goals.home' / 'goals.away' (optional)
    """
    # Standardisiere Home/Away-Teams
    if 'team_h' in df.columns:
        df['home_team_std'] = df['team_h'].apply(standardize_team)
    if 'team_a' in df.columns:
        df['away_team_std'] = df['team_a'].apply(standardize_team)
    
    rename_dict = {}
    for col in df.columns:
        if col.startswith('h_'):
            rename_dict[col] = 'home_' + col[2:]
        elif col.startswith('a_'):
            rename_dict[col] = 'away_' + col[2:]
    df.rename(columns=rename_dict, inplace=True)
    
    if 'home_goals' in df.columns:
        df.rename(columns={'home_goals': 'goals.home'}, inplace=True)
    if 'away_goals' in df.columns:
        df.rename(columns={'away_goals': 'goals.away'}, inplace=True)
    
    return df


def prepare_filtered_match_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardisiert das CSV 'filtered_MatchData':
      - 'home_team' => 'home_team_std', 'away_team' => 'away_team_std'
      - 'home_goals' => 'score.fulltime.home', 'away_goals' => 'score.fulltime.away'
        => unify_goal_columns => 'goals.home'/'goals.away'
    """
    if 'home_team' in df.columns:
        df['home_team_std'] = df['home_team'].apply(standardize_team)
    if 'away_team' in df.columns:
        df['away_team_std'] = df['away_team'].apply(standardize_team)
    
    if 'home_goals' in df.columns:
        df.rename(columns={'home_goals': 'score.fulltime.home'}, inplace=True)
    if 'away_goals' in df.columns:
        df.rename(columns={'away_goals': 'score.fulltime.away'}, inplace=True)

    df = unify_goal_columns(df)
    return df


def run_data_processing_pipeline(
    teams_csv: str = None,
    players_csv: str = None,
    matches_csv: str = None,
    match_data_csv: str = None,
    use_table: bool = False,
    league: str = "bl1",
    season: str = "2024",
    api_key: str = "2cedf059b44f953884d6476e481b8009"
):
    """
    Erweitertes Pipeline-Skript, das alle 4 CSV-Dateien lädt und standardisiert:
      1) Teams (filtered_TeamsData.csv)
      2) Spieler (filtered_PlayersData_perYear.csv)
      3) Matches (filtered_Matches.csv)
      4) MatchData (filtered_MatchData.csv)

    - Falls use_table=True: Bundesliga-Tabelle (OpenLigaDB) -> team_data
    - Falls use_table=False: Merge ApiSports-Daten + Teams-CSV -> unify -> prepare_team_data -> team_data
    - Spieler-Daten -> standardisieren -> team_players
    - Matches-Daten -> standardisieren -> df_matches
    - MatchData -> standardisieren -> df_match_data

    Rückgabe:
      (team_data, team_players, df_matches, df_match_data)
    """
    script_dir = os.path.dirname(__file__)
    
    if teams_csv is None:
        teams_csv = os.path.join(script_dir, "../../data/filtercsv/filtered_TeamsData.csv")
    if players_csv is None:
        players_csv = os.path.join(script_dir, "../../data/filtercsv/filtered_PlayersData_perYear.csv")
    if matches_csv is None:
        matches_csv = os.path.join(script_dir, "../../data/filtercsv/filtered_Matches.csv")
    if match_data_csv is None:
        match_data_csv = os.path.join(script_dir, "../../data/filtercsv/filtered_MatchData.csv")

    if use_table:
        df_table = get_current_bundesliga_table(league, season)
        print("DEBUG: Aktuelle Tabelle shape:", df_table.shape)
        team_data = {}
        for _, row in df_table.iterrows():
            raw_team = row.get("teamName")
            if not raw_team:
                continue
            std_team = standardize_team(raw_team)
            team_data[std_team] = {
                "stats": row.to_dict(),
                "matches": pd.DataFrame()
            }
    else:
        df_merged = merge_api_csv(api_key, league_id=78, season=2022, csv_path=teams_csv)
        print("DEBUG: Gemergter DataFrame shape:", df_merged.shape)
        print("DEBUG: Gemergte Spalten:", df_merged.columns.tolist())

        if df_merged.empty:
            print("WARNUNG: Der gemergte DataFrame ist leer.")
            return {}, {}, pd.DataFrame(), pd.DataFrame()

        df_merged = unify_goal_columns(df_merged)
        team_data = prepare_team_data(df_merged)

    players_df = pd.read_csv(players_csv)
    if "team_title" in players_df.columns:
        players_df["team_name_std"] = players_df["team_title"].apply(standardize_team)
    team_players = prepare_player_data(players_df)

    df_matches = pd.read_csv(matches_csv)
    df_matches = prepare_filtered_matches(df_matches)

    df_match_data = pd.read_csv(match_data_csv)
    df_match_data = prepare_filtered_match_data(df_match_data)

    return team_data, team_players, df_matches, df_match_data


if __name__ == "__main__":
    print("=== Tabellen-Modus ===")
    td_table, tp_table, matches_table, mdata_table = run_data_processing_pipeline(use_table=True)
    print(f"TeamData Keys (Tabellenmodus): {list(td_table.keys())[:5]}")
    print(f"Matches shape: {matches_table.shape}, MatchData shape: {mdata_table.shape}")

    print("\n=== Klassischer Modus (ApiSports) ===")
    td_api, tp_api, matches_api, mdata_api = run_data_processing_pipeline(use_table=False)
    print(f"TeamData Keys (Klassisch): {list(td_api.keys())[:5]}")
    print(f"Matches shape: {matches_api.shape}, MatchData shape: {mdata_api.shape}")
