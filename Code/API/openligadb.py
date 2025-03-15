import json
import logging
import os

import pandas as pd
import requests
from team_mapping import standardize_team


class OpenLigaDBClient:
    def __init__(self, league="bl1", season="2024", data_dir="data/openligadb"):
        self.base_url = "https://api.openligadb.de/"
        self.league = league
        self.season = season
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def get_match_data(self, matchday):
        """
        Ruft die Spieldaten für einen bestimmten Spieltag ab und speichert sie als JSON.
        """
        endpoint = f"getmatchdata/{self.league}/{self.season}/{matchday}"
        url = self.base_url + endpoint
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            file_path = os.path.join(self.data_dir, f"matchday_{matchday}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Fehler beim Abruf der Daten für Spieltag {matchday}: {e}")
            return None

    def get_all_matchdays(self, matchdays):
        """
        Ruft für eine Liste von Spieltagen die Daten ab und fügt sie in einer Liste zusammen.
        """
        all_matches = []
        for md in matchdays:
            data = self.get_match_data(md)
            if data:
                all_matches.extend(data)
        return all_matches

    def matches_to_df(self, match_data):
        """
        Wandelt die abgerufenen Match-Daten in ein pandas DataFrame um.
        Dabei werden auch die Teamnamen standardisiert.
        """
        df = pd.json_normalize(match_data)
        if "Team1.TeamName" in df.columns:
            df["home_team_std"] = df["Team1.TeamName"].apply(standardize_team)
        if "Team2.TeamName" in df.columns:
            df["away_team_std"] = df["Team2.TeamName"].apply(standardize_team)
        return df

if __name__ == "__main__":
    client = OpenLigaDBClient()
    all_matchdays = client.get_all_matchdays(matchdays=range(1, 35))
    df_matches = client.matches_to_df(all_matchdays)
    print("Abgerufene Daten:")
    print(df_matches.head())
