import pandas as pd
import pytest
from src.data.data_processing import (
    unify_goal_columns,
    prepare_filtered_matches,
    prepare_filtered_match_data,
    prepare_player_data,
    compute_team_stats
)

@pytest.fixture
def sample_match_df():
    return pd.DataFrame({
        "home_team_std": ["team a", "team b", "team a"],
        "away_team_std": ["team b", "team a", "team c"],
        "goals.home": [2, 1, 3],
        "goals.away": [1, 1, 0],
        "xG": [1.5, 0.9, 2.3],
        "xGA": [1.2, 1.1, 0.7]
    })

def test_unify_goal_columns_score_columns():
    df = pd.DataFrame({
        "score.fulltime.home": [1],
        "score.fulltime.away": [2]
    })
    df = unify_goal_columns(df)
    assert "goals.home" in df.columns
    assert df["goals.home"].iloc[0] == 1

def test_prepare_filtered_matches_column_renaming():
    df = pd.DataFrame({
        "team_h": ["FC Bayern"],
        "team_a": ["BVB"],
        "h_goals": [2],
        "a_goals": [1]
    })
    result = prepare_filtered_matches(df.copy())
    assert "home_team_std" in result.columns
    assert "goals.home" in result.columns

def test_prepare_filtered_match_data_renaming():
    df = pd.DataFrame({
        "home_team": ["FC Bayern"],
        "away_team": ["BVB"],
        "home_goals": [3],
        "away_goals": [1]
    })
    result = prepare_filtered_match_data(df)
    assert "goals.home" in result.columns
    assert result["goals.home"].iloc[0] == 3

def test_prepare_player_data_grouping():
    df = pd.DataFrame({
        "team_name_std": ["Team A", "Team A", "Team B"],
        "player": ["A", "B", "C"]
    })
    grouped = prepare_player_data(df)
    assert len(grouped) == 2
    assert grouped["Team A"].shape[0] == 2

def test_compute_team_stats_basic(sample_match_df):
    stats = compute_team_stats(sample_match_df, "team a", metrics=["xG", "xGA"])
    assert isinstance(stats, dict)
    assert "stats" in stats
    assert stats["stats"]["wins"] >= 0
    assert stats["stats"]["avg_xG"] is not None
