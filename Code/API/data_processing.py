import os
import pandas as pd

from .merge_data import merge_api_csv 
from .openligadb_table import get_current_bundesliga_table  
from .team_mapping import standardize_team


def unify_goal_columns(df):
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
        print("WARNUNG: Weder 'goals.home'/'goals.away' noch 'score.fulltime.home'/'score.fulltime.away' vorhanden.")
        print("Evtl. liegen die Tore anderswo (z.B. in 'goals' als Liste).")

    if "goals.home" in df.columns:
        df["goals.home"] = pd.to_numeric(df["goals.home"], errors="coerce")
    if "goals.away" in df.columns:
        df["goals.away"] = pd.to_numeric(df["goals.away"], errors="coerce")
        
    print("DEBUG unify_goal_columns: columns after rename:", df.columns.tolist(), "\n")
    return df


def prepare_team_data(df):
    """
    Aggregiert die Spielstatistiken für jedes Team aus dem gemergten DataFrame.
    Nutzt:
      - 'home_team_std' / 'away_team_std' für die Teamzuordnung
      - 'goals.home' / 'goals.away' für die Tore
      - ggf. Metriken wie xG, xGA, etc., falls vorhanden.
    
    Zusätzlich werden die Tordifferenz und Punkte (3 Punkte pro Sieg, 1 Punkt pro Unentschieden) berechnet.
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
        
        wins = 0
        draws = 0
        losses = 0
        goals_scored = 0
        goals_conceded = 0
        metric_sums = {m: 0.0 for m in metrics}
        
        for _, row in team_matches.iterrows():
            if row['home_team_std'] == team:
                goals_scored += row['goals.home']
                goals_conceded += row['goals.away']
                if row['goals.home'] > row['goals.away']:
                    wins += 1
                elif row['goals.home'] == row['goals.away']:
                    draws += 1
                else:
                    losses += 1
                for m in metrics:
                    metric_sums[m] += row[m]
            else:
                goals_scored += row['goals.away']
                goals_conceded += row['goals.home']
                if row['goals.away'] > row['goals.home']:
                    wins += 1
                elif row['goals.away'] == row['goals.home']:
                    draws += 1
                else:
                    losses += 1
                for m in metrics:
                    metric_sums[m] += row[m]
        
        num_matches = len(team_matches)
        averages = {f"avg_{m}": metric_sums[m] / num_matches if num_matches > 0 else None for m in metric_sums}
        
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


def prepare_player_data(players_df):
    """
    Gruppiert die Spielerdaten nach dem standardisierten Teamnamen (Spalte 'team_name_std').
    """
    team_players = {}
    if "team_name_std" in players_df.columns:
        for team, group in players_df.groupby("team_name_std"):
            team_players[team] = group.reset_index(drop=True)
    else:
        for team, group in players_df.groupby("team_title"):
            team_players[team] = group.reset_index(drop=True)
    return team_players


def run_data_processing_pipeline(
    teams_csv=None,
    players_csv=None,
    use_table=False,
    league="bl1",
    season="2024",
    api_key="2cedf059b44f953884d6476e481b8009"
):
    """
    Führt den gesamten Datenverarbeitungsprozess aus:
      - Falls use_table True: Abrufen der aktuellen Bundesliga-Tabelle (OpenLigaDB)
        und Erzeugung von team_data direkt aus der Tabelle.
      - Falls use_table False: Merge von ApiSports-Daten (Fixtures) mit den historischen CSV-Daten,
        Vereinheitlichen der Tor-Spalten und Aggregation der Team-Statistiken.
      - Laden der Spielerdaten und Gruppierung nach Team.
    """
    script_dir = os.path.dirname(__file__)
    if teams_csv is None:
        teams_csv = os.path.join(script_dir, "../../data/filtercsv/filtered_TeamsData.csv")
    if players_csv is None:
        players_csv = os.path.join(script_dir, "../../data/filtercsv/filtered_PlayersData_perYear.csv")
    
    if use_table:
        df_table = get_current_bundesliga_table(league, season)
        print("DEBUG: Aktuelle Tabelle shape:", df_table.shape)
        
        team_data = {}
        for _, row in df_table.iterrows():
            team = row.get("teamName")
            if not team:
                continue
            std_team = standardize_team(team)
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
            return {}, {}
        
        df_merged = unify_goal_columns(df_merged)
        team_data = prepare_team_data(df_merged)

    players_df = pd.read_csv(players_csv)
    if "team_title" in players_df.columns:
        players_df["team_name_std"] = players_df["team_title"].apply(standardize_team)

    team_players = prepare_player_data(players_df)
    
    return team_data, team_players


if __name__ == "__main__":
    print("=== Tabellen-Modus ===")
    team_data, team_players = run_data_processing_pipeline(use_table=True)
    for t, data in team_data.items():
        print(f"Team: {t}")
        print("Stats:", data["stats"])
        break

    print("\n=== Klassischer Modus (ApiSports) ===")
    team_data, team_players = run_data_processing_pipeline(use_table=False)
    for t, data in team_data.items():
        print(f"Team: {t}")
        print("Stats:", data["stats"])
        break
