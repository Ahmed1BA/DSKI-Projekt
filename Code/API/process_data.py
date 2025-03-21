import json


def process(team_id_1, team_id_2):
    with open(f"daten/{team_id_1},{team_id_2}.json", "r") as file:
        data = json.load(file)

    spiele_daten = []

    for match in data["response"]:
        fixture = match["fixture"]
        league = match["league"]
        teams = match["teams"]
        goals = match["goals"]
        halftime = match["score"]["halftime"]

        if teams["home"]["winner"]:
            winner = teams["home"]["name"]
        elif teams["away"]["winner"]:
            winner = teams["away"]["name"]
        else:
            winner = "Unentschieden"

        spiel = {
            "Datum": fixture["date"],
            "Saison": league["season"],
            "Stadion": fixture["venue"]["name"],
            "Heimteam": teams["home"]["name"],
            "Auswärtsteam": teams["away"]["name"],
            "Ergebnis": f"{goals['home']} - {goals['away']}",
            "Halbzeit": f"{halftime['home']} - {halftime['away']}",
            "Siegerteam": winner
        }

        spiele_daten.append(spiel)
    with open(f"processed_data/processed_data{team_id_1}_{team_id_2}.json", "w") as file:
        json.dump(spiele_daten, file)
    print(data)


process(172, 160)
