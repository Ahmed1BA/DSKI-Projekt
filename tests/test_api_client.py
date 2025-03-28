import os
from unittest.mock import patch, MagicMock
import json
import pytest
from Code.API.api_client import ApiSportsClient
from requests.exceptions import RequestException

@pytest.fixture
def client(tmp_path):
    return ApiSportsClient(api_key="FAKE_KEY", data_dir=tmp_path)

@patch("Code.API.api_client.requests.get")
def test_get_league_data_success(mock_get, client, tmp_path):
    fake_response = {"response": [{"league": {"id": 78}}]}
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = fake_response

    data = client.get_league_data(78)
    
    assert data == fake_response
    file_path = tmp_path / "leagues" / "78.json"
    assert file_path.exists()
    
    with open(file_path, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == fake_response

@patch("Code.API.api_client.requests.get")
def test_get_team_data_error(mock_get, client):
    mock_get.side_effect = RequestException("Network error")

    result = client.get_team_data(42)
    assert result is None

@patch("Code.API.api_client.requests.get")
def test_get_headtohead_data_format(mock_get, client):
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = {"response": []}

    data = client.get_headtohead_data(1, 2)
    assert isinstance(data, dict)

@patch("Code.API.api_client.requests.get")
def test_get_fixtures_file_written(mock_get, client, tmp_path):
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = {"response": [{"match": 1}]}

    data = client.get_fixtures(78, 2023)
    assert "response" in data

    file_path = tmp_path / "fixtures" / "78_2023.json"
    assert file_path.exists()
