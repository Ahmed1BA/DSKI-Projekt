import os
import pandas as pd
import logging

from ..data.merge_data import merge_api_csv
from ..api.openligadb_table import get_current_bundesliga_table
from ..mapping.team_mapping import standardize_team
from ..api.api_key import API_KEY

GOALS_HOME = "goals.home"
GOALS_AWAY = "goals.away"
SCORE_HOME = "score.fulltime.home"
SCORE_AWAY = "score.fulltime.away"


def unify_goal_columns(df: pd.DataFrame) -> pd.DataFrame:
    logging.debug("Spalten vor Umbenennung: %s", df.columns.tolist())

    if GOALS_HOME in df.columns and GOALS_AWAY in df.columns:
        logging.debug("'%s'/'%s' sind bereits vorhanden.", GOALS_HOME, GOALS_AWAY)
    elif SCORE_HOME in df.columns and SCORE_AWAY in df.columns:
        logging.debug("Benenne '%s'/'%s' → '%s'/'%s'", SCORE_HOME, SCORE_AWAY, GOALS_HOME, GOALS_AWAY)
        df.rename(columns={SCORE_HOME: GOALS_HOME, SCORE_AWAY: GOALS_AWAY}, inplace=True)
    else:
        logging.warning("Keine bekannten Tore-Spalten gefunden.")

    if GOALS_HOME in df.columns:
        df[GOALS_HOME] = pd.to_numeric(df[GOALS_HOME], errors="coerce")
    if GOALS_AWAY in df.columns:
        df[GOALS_AWAY] = pd.to_numeric(df[GOALS_AWAY], errors="coerce")

    logging.debug("Spalten nach Umbenennung: %s", df.columns.tolist())
    return df


def compute_team_stats(df: pd.DataFrame, team: str, metrics: list) -> dict:
    team_matches = df[(df['home_team_std'] == team) | (df['away_team_std'] == team)]

    wins = draws = losses = 0
    goals_scored = goals_conceded = 0
    metric_sums = {m: 0.0 for m in metrics}

    for _, row in team_matches.iterrows():
        is_home = row['home_team_std'] == team
        home_goals = row.get(GOALS_HOME, 0)
        away_goals = row.get(GOALS_AWAY, 0)

        scored = home_goals if is_home else away_goals
        conceded = away_goals if is_home else home_goals

        goals_scored += scored
        goals_conceded += conceded

        if scored > conceded:
            wins += 1
        elif scored == conceded:
            draws += 1
        else:
            losses += 1

        for m in metrics:
            metric_sums[m] += row[m]

    num_matches = len(team_matches)
    averages = {
        f"avg_{m}": (metric_sums[m] / num_matches) if num_matches > 0 else None
        for m in metrics
    }

    stats = {
        'matches': num_matches,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'goals_scored': goals_scored,
        'goals_conceded': goals_conceded,
        'goal_difference': goals_scored - goals_conceded,
        'points': wins * 3 + draws,
        **averages
    }

    return {
        'matches': team_matches,
        'stats': stats
    }


def prepare_team_data(df: pd.DataFrame) -> dict:
    teams = set(df['home_team_std']).union(set(df['away_team_std']))

    metrics = [
        'xG', 'xGA', 'npxG', 'npxGA', 'ppda_att', 'ppda_def',
        'ppda_allowed_att', 'ppda_allowed_def', 'deep', 'deep_allowed',
        'scored', 'missed', 'xpts', 'npxGD'
    ]
    metrics = [m for m in metrics if m in df.columns]

    return {team: compute_team_stats(df, team, metrics) for team in teams}


def prepare_player_data(players_df: pd.DataFrame) -> dict:
    team_players = {}
    group_col = "team_name_std" if "team_name_std" in players_df.columns else "team_title"

    for team, group in players_df.groupby(group_col):
        team_players[team] = group.reset_index(drop=True)

    return team_players


def prepare_filtered_matches(df: pd.DataFrame) -> pd.DataFrame:
    if 'team_h' in df.columns:
        df['home_team_std'] = df['team_h'].apply(standardize_team)
    if 'team_a' in df.columns:
        df['away_team_std'] = df['team_a'].apply(standardize_team)

    rename_dict = {
        col: 'home_' + col[2:] if col.startswith('h_') else 'away_' + col[2:]
        for col in df.columns if col.startswith(('h_', 'a_'))
    }
    df.rename(columns=rename_dict, inplace=True)

    df.rename(columns={
        'home_goals': GOALS_HOME,
        'away_goals': GOALS_AWAY
    }, inplace=True)

    return df


def prepare_filtered_match_data(df: pd.DataFrame) -> pd.DataFrame:
    if 'home_team' in df.columns:
        df['home_team_std'] = df['home_team'].apply(standardize_team)
    if 'away_team' in df.columns:
        df['away_team_std'] = df['away_team'].apply(standardize_team)

    df.rename(columns={
        'home_goals': SCORE_HOME,
        'away_goals': SCORE_AWAY
    }, inplace=True)

    return unify_goal_columns(df)


def run_data_processing_pipeline(
    teams_csv: str = None,
    players_csv: str = None,
    matches_csv: str = None,
    match_data_csv: str = None,
    use_table: bool = False,
    league: str = "bl1",
    season: str = "2024",
    api_key: str = API_KEY
):
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(script_dir, "../../docs/filtercsv"))

    teams_csv = teams_csv or os.path.join(data_dir, "filtered_TeamsData.csv")
    players_csv = players_csv or os.path.join(data_dir, "filtered_PlayersData_perYear.csv")
    matches_csv = matches_csv or os.path.join(data_dir, "filtered_Matches.csv")
    match_data_csv = match_data_csv or os.path.join(data_dir, "filtered_MatchData.csv")

    if use_table:
        df_table = get_current_bundesliga_table(league, season)
        logging.info("Tabelle geladen, Shape: %s", df_table.shape)
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
        logging.info("Gemergter DataFrame geladen, Shape: %s", df_merged.shape)

        if df_merged.empty:
            logging.warning("Gemergter DataFrame ist leer – Abbruch.")
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
    from ..logging_config import setup_logging
    setup_logging("logs/data_processing.log")

    logging.info("=== Tabellen-Modus ===")
    td_table, tp_table, matches_table, mdata_table = run_data_processing_pipeline(use_table=True)
    logging.info("Teams (Tabelle): %d | Matches: %d | MatchData: %d",
                 len(td_table), matches_table.shape[0], mdata_table.shape[0])

    logging.info("=== Klassischer Modus (ApiSports) ===")
    td_api, tp_api, matches_api, mdata_api = run_data_processing_pipeline(use_table=False)
    logging.info("Teams (API): %d | Matches: %d | MatchData: %d",
                 len(td_api), matches_api.shape[0], mdata_api.shape[0])
