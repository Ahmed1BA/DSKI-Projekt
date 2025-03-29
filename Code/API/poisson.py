import requests
import numpy as np
from scipy.stats import poisson
from DSKI_Projekt.Code.API.team_mapping import standardize_team

API_URL = "https://api.openligadb.de/getmatchdata/bl1"

def fetch_all_finished_matches(league="bl1", season=2024, max_matchday=34):
    all_matches = []
    for matchday in range(1, max_matchday + 1):
        url = f"{API_URL}/{season}/{matchday}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        matches = r.json()
        finished = [m for m in matches if m.get("matchIsFinished")]
        all_matches.extend(finished)
    return all_matches

def extract_goals(matches):
    teams = {}
    for m in matches:
        final_result = None
        for res in m.get("matchResults", []):
            if res.get("resultTypeID") == 2:
                final_result = res
                break
        if not final_result:
            continue
        t1 = standardize_team(m.get("team1", {}).get("teamName", ""))
        t2 = standardize_team(m.get("team2", {}).get("teamName", ""))
        if t1:
            if t1 not in teams:
                teams[t1] = {"home": [], "away": []}
            teams[t1]["home"].append(final_result.get("pointsTeam1", 0))
        if t2:
            if t2 not in teams:
                teams[t2] = {"home": [], "away": []}
            teams[t2]["away"].append(final_result.get("pointsTeam2", 0))
    return teams

def calc_poisson_distribution(avg, max_goals=5):
    x = np.arange(max_goals + 1)
    return poisson.pmf(x, avg)

def calc_poisson_for_all_teams(league="bl1", season=2024, max_matchday=34, max_goals=5):
    matches = fetch_all_finished_matches(league, season, max_matchday)
    teams_data = extract_goals(matches)
    results = {}
    for team, data in teams_data.items():
        avg_home = np.mean(data["home"]) if data["home"] else 0
        avg_away = np.mean(data["away"]) if data["away"] else 0
        poisson_home = calc_poisson_distribution(avg_home, max_goals)
        poisson_away = calc_poisson_distribution(avg_away, max_goals)
        results[team] = {
            "avg_home": avg_home,
            "avg_away": avg_away,
            "poisson_home": poisson_home,
            "poisson_away": poisson_away
        }
    return results
