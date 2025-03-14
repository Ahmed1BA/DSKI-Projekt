



# CODE ALT , BEHALTEN BIS NEUER CODE IN "api_client.py" FUNKTIONIERT




# import json
# import dictionary as dic

# import requests

# api_key = '2cedf059b44f953884d6476e481b8009'
# base_url = 'https://v3.football.api-sports.io/'
# headers = {
#     'x-apisports-key': api_key
# }


# def einfaches_verbinden():
#     endpoint = 'leagues'
#     response = requests.get(base_url + endpoint, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         # print(data)
#     else:
#         print(f"Error: {response.status_code}")


# def liga_aufrufen(league_id):
#     endpoint = f'leagues?id={league_id}'
#     response = requests.get(base_url + endpoint, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#         with open(f"daten/{league_id}.json", "w") as outfile:
#             json.dump(data, outfile)
#         print(data)
#     else:
#         print(f"Fehler: {response.status_code}")


# def mannschaft_aufrufen(team_id):
#     """
#     ruft Daten einer Mannschaft auf
#     :param team_id: gewünschte Mannschaft
#     :return:
#     """
#     endpoint = f'teams?id={team_id}'
#     response = requests.get(base_url + endpoint, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#         with open(f"daten/{team_id}.json", "w") as outfile:
#             json.dump(data, outfile)
#         print(data)
#     else:
#         print(f"Fehler: {response.status_code}")


# def spieldaten_2_mannschaften(team_id_1, team_id_2):
#     """
#     ruft alle Daten der vergangenen begegnungen auf
#     :param team_id_1: id der Heimmannschaft
#     :param team_id_2: id der Auswärtsmannschaft
#     :return:
#     """
#     endpoint = f'fixtures/headtohead?h2h={team_id_2}-{team_id_1}'
#     response = requests.get(base_url + endpoint, headers=headers)
#     if response.status_code == 200:

#         data = response.json()
#         print(data)
#         with open(f"daten/{team_id_1},{team_id_2}.json", "w") as outfile:
#             json.dump(data, outfile)
#     else:
#         print(f"Fehler: {response.status_code}")


# liga_aufrufen(78)
# mannschaft_aufrufen(dic.team_ids_bundesliga["FC Bayern München"])
# spieldaten_2_mannschaften(172, 160)
