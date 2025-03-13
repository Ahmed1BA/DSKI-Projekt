import json
import dictionary as dic

import requests

api_key = '2cedf059b44f953884d6476e481b8009'
base_url = 'https://v3.football.api-sports.io/'
headers = {
    'x-apisports-key': api_key
}


def einfaches_verbinden():
    endpoint = 'leagues'
    response = requests.get(base_url + endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}")


def liga_aufrufen(league_id):
    endpoint = f'leagues?id={league_id}'
    response = requests.get(base_url + endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json()
        with open(f"daten/{league_id}.json", "w") as outfile:
            json.dump(data, outfile)
        print(data)
    else:
        print(f"Fehler: {response.status_code}")


def mannschaft_aufrufen(team_id):
    endpoint = f'teams?id={team_id}'
    response = requests.get(base_url + endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json()
        with open(f"daten/{team_id}.json", "w") as outfile:
            json.dump(data, outfile)
        print(data)
    else:
        print(f"Fehler: {response.status_code}")


liga_aufrufen(78)
mannschaft_aufrufen(dic.team_ids_bundesliga["FC Bayern München"])
