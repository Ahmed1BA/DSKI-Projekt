from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from Code.API.openligadb_table import get_current_bundesliga_table

@patch("Code.API.openligadb_table.requests.get")
def test_get_current_bundesliga_table_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"teamName": "FC Bayern", "points": 55},
        {"teamName": "BVB", "points": 53}
    ]
    mock_get.return_value = mock_response

    df = get_current_bundesliga_table()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "teamName" in df.columns

@patch("Code.API.openligadb_table.requests.get")
def test_get_current_bundesliga_table_empty_response(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    with pytest.raises(ValueError):
        get_current_bundesliga_table()

@patch("Code.API.openligadb_table.requests.get", side_effect=Exception("API Down"))
def test_get_current_bundesliga_table_error(mock_get):
    with pytest.raises(Exception):
        get_current_bundesliga_table()
