from unittest.mock import patch
import pandas as pd
import pytest
from src.data.merge_data import load_fixtures_to_df, merge_api_csv

@pytest.fixture
def sample_csv(tmp_path):
    path = tmp_path / "teams.csv"
    path.write_text("team_title\nFC Bayern\nBorussia Dortmund")
    return path

@pytest.fixture
def mock_api_response():
    return {
        "response": [
            {
                "teams": {
                    "home": {"name": "FC Bayern"},
                    "away": {"name": "Borussia Dortmund"}
                }
            }
        ]
    }

@patch("Code.API.merge_data.ApiSportsClient")
def test_load_fixtures_to_df_success(mock_client_class, mock_api_response):
    mock_client = mock_client_class.return_value
    mock_client.get_fixtures.return_value = mock_api_response

    df = load_fixtures_to_df("fake_key", 78, 2023)
    assert not df.empty
    assert "home_team_std" in df.columns
    assert df["home_team_std"].iloc[0] == "bayern münchen"

@patch("Code.API.merge_data.ApiSportsClient")
def test_load_fixtures_to_df_no_data(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.get_fixtures.return_value = None

    df = load_fixtures_to_df("fake_key", 78, 2023)
    assert df.empty

@patch("Code.API.merge_data.load_fixtures_to_df")
@patch("Code.API.merge_data.load_csv_data")
def test_merge_api_csv_success(mock_load_csv, mock_load_api, sample_csv):
    df_api = pd.DataFrame({
        "home_team_std": ["bayern münchen"],
        "teams.home.name": ["FC Bayern"]
    })

    df_csv = pd.DataFrame({
        "team_title": ["FC Bayern"],
        "team_name_std": ["bayern münchen"],
        "info": ["Test"]
    })

    mock_load_api.return_value = df_api
    mock_load_csv.return_value = df_csv

    merged = merge_api_csv("key", 78, 2022, sample_csv)
    assert not merged.empty
    assert "info" in merged.columns

@patch("Code.API.merge_data.load_fixtures_to_df", return_value=pd.DataFrame())
@patch("Code.API.merge_data.load_csv_data", return_value=pd.DataFrame())
def test_merge_api_csv_fails_with_empty_data(_, __, sample_csv):
    result = merge_api_csv("key", 78, 2022, sample_csv)
    assert result.empty
