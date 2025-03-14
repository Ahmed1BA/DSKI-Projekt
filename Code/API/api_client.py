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

    def get_league_data(self, league_id):
        endpoint = f"leagues?id={league_id}"
        url = self.base_url + endpoint
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            file_path = os.path.join(self.leagues_dir, f"{league_id}.json")
            with open(file_path, "w") as f:
                json.dump(data, f)
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching league data: {e}")
            return None

    def get_team_data(self, team_id):
        endpoint = f"teams?id={team_id}"
        url = self.base_url + endpoint
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            file_path = os.path.join(self.teams_dir, f"{team_id}.json")
            with open(file_path, "w") as f:
                json.dump(data, f)
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching team data: {e}")
            return None

    def get_headtohead_data(self, team_id1, team_id2):
        endpoint = f"fixtures/headtohead?h2h={team_id2}-{team_id1}"
        url = self.base_url + endpoint
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            file_path = os.path.join(self.fixtures_dir, f"{team_id1}_{team_id2}.json")
            with open(file_path, "w") as f:
                json.dump(data, f)
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching head-to-head data: {e}")
            return None
