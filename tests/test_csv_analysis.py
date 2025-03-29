from unittest.mock import patch

import pandas as pd
import pytest

from src.analysis.csv_analysis import load_csv_data, load_all_filtered_csvs, analyze_csv_data

SAMPLE_CSV = "team_title,goals\nFC Bayern,3\nBorussia Dortmund,2"

@pytest.fixture
def tmp_csv_file(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text(SAMPLE_CSV)
    return file

def test_load_csv_success(tmp_csv_file):
    df = load_csv_data(str(tmp_csv_file), team_col="team_title")
    assert not df.empty
    assert "team_name_std" in df.columns
    assert df.iloc[0]["team_name_std"] == "bayern münchen"

def test_load_csv_missing_file(tmp_path):
    df = load_csv_data(str(tmp_path / "non_existing.csv"))
    assert df.empty

def test_load_csv_no_team_col(tmp_csv_file):
    df = load_csv_data(str(tmp_csv_file), team_col="nonexistent")
    assert "team_name_std" not in df.columns

def test_load_all_filtered_csvs_creates_four_keys(tmp_path):
    (tmp_path / "filtered_MatchData.csv").write_text("match_id\n")
    (tmp_path / "filtered_TeamsData.csv").write_text("team_title\nFC Bayern")
    (tmp_path / "filtered_PlayersData_perYear.csv").write_text("player_name\n")
    (tmp_path / "filtered_Matches.csv").write_text("match_id\n")

    dfs = load_all_filtered_csvs(tmp_path)
    assert len(dfs) == 4
    assert all(isinstance(df, pd.DataFrame) for df in dfs)

@patch("Code.API.csv_analysis.logging")
def test_analyze_csv_data_logging(mock_log):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    analyze_csv_data(df, label="TestFrame")
    mock_log.info.assert_any_call("=== Analyse: %s ===", "TestFrame")
    mock_log.info.assert_any_call("Shape: %s", df.shape)
    mock_log.info.assert_any_call("Spalten: %s", df.columns.tolist())
