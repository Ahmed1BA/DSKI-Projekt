import json
import os
import logging
import requests

class ApiSportsClient:
    def __init__(self, api_key, data_dir="data"):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io/"
        self.headers = {"x-apisports-key": self.api_key}
        self.data_dir = data_dir
        self.leagues_dir = os.path.join(self.data_dir, "leagues")
        self.teams_dir = os.path.join(self.data_dir, "teams")
        self.fixtures_dir = os.path.join(self.data_dir, "fixtures")
        os.makedirs(self.leagues_dir, exist_ok=True)
        os.makedirs(self.teams_dir, exist_ok=True)
        os.makedirs(self.fixtures_dir, exist_ok=True)

    def _fetch_and_save(self, endpoint: str, file_path: str):
        url = self.base_url + endpoint
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            return data
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching data from %s: %s", endpoint, e)
            return None

    def get_league_data(self, league_id):
        endpoint = f"leagues?id={league_id}"
        file_path = os.path.join(self.leagues_dir, f"{league_id}.json")
        return self._fetch_and_save(endpoint, file_path)

    def get_team_data(self, team_id):
        endpoint = f"teams?id={team_id}"
        file_path = os.path.join(self.teams_dir, f"{team_id}.json")
        return self._fetch_and_save(endpoint, file_path)

    def get_headtohead_data(self, team_id1, team_id2):
        endpoint = f"fixtures/headtohead?h2h={team_id2}-{team_id1}"
        file_path = os.path.join(self.fixtures_dir, f"{team_id1}_{team_id2}.json")
        return self._fetch_and_save(endpoint, file_path)

    def get_fixtures(self, league_id, season):
        endpoint = f"fixtures?league={league_id}&season={season}"
        file_path = os.path.join(self.fixtures_dir, f"{league_id}_{season}.json")
        return self._fetch_and_save(endpoint, file_path)
