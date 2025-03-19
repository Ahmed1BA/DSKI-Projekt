import json
import logging
import os

import pandas as pd
import requests
from Code.API.team_mapping import standardize_team


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
        Wandelt die JSON-Daten der Spiele in ein DataFrame um und versucht,
        die Teamnamen (Heim/Auswärts) zu identifizieren und zu standardisieren.
        """
        df = pd.json_normalize(match_data)
        print("DEBUG: OpenLigaDB-Spalten:", df.columns.tolist())

        possible_team1_cols = [
            "Team1.TeamName",   
            "team1.teamName",   
            "Team1",            
            "team1",           
            "nameTeam1"         
        ]
        for col in possible_team1_cols:
            if col in df.columns:
                print(f"DEBUG: Verwende Spalte '{col}' für das Heimteam.")
                if col in ["Team1", "team1"]:
                    df["Team1.TeamName"] = df[col].apply(
                        lambda x: x.get("teamName") or x.get("TeamName") if isinstance(x, dict) else None
                    )
                    df["home_team_std"] = df["Team1.TeamName"].apply(standardize_team)
                else:
                    df["home_team_std"] = df[col].apply(standardize_team)
                break
        else:
            print("WARNUNG: Keine geeignete Spalte für das Heimteam gefunden.")

        possible_team2_cols = [
            "Team2.TeamName",
            "team2.teamName",
            "Team2",
            "team2",
            "nameTeam2"
        ]
        for col in possible_team2_cols:
            if col in df.columns:
                print(f"DEBUG: Verwende Spalte '{col}' für das Auswärtsteam.")
                if col in ["Team2", "team2"]:
                    df["Team2.TeamName"] = df[col].apply(
                        lambda x: x.get("teamName") or x.get("TeamName") if isinstance(x, dict) else None
                    )
                    df["away_team_std"] = df["Team2.TeamName"].apply(standardize_team)
                else:
                    df["away_team_std"] = df[col].apply(standardize_team)
                break
        else:
            print("WARNUNG: Keine geeignete Spalte für das Auswärtsteam gefunden.")

        return df


if __name__ == "__main__":
    client = OpenLigaDBClient()
    all_matchdays = client.get_all_matchdays(matchdays=range(1, 35))
    df_matches = client.matches_to_df(all_matchdays)
    print("Abgerufene Daten:")
    print(df_matches.head())
