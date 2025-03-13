import requests
import json

def get_data():
    api_key = 'api key'
    url = f"URL{api_key}"
    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

get_data()