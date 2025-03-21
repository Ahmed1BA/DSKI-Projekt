import requests
import pandas as pd

def get_current_bundesliga_table(league="bl1", season="2024"):
    """
    Ruft die aktuelle Bundesliga-Tabelle (inoffiziell) von OpenLigaDB ab.
    
    Parameters:
        league (str): Liga-Kürzel, z.B. "bl1" für die Bundesliga.
        season (str): Saison, z.B. "2024".
    
    Returns:
        pd.DataFrame: Tabelle als DataFrame, z.B. mit Feldern wie teamName, tablePlace, points, won, draw, lost, goals, opponentGoals, etc.
    """
    url = f"https://www.openligadb.de/api/getbltable/{league}/{season}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Fehler beim Abrufen der Tabelle: HTTP {response.status_code}")
    
    table_json = response.json()
    if not isinstance(table_json, list) or len(table_json) == 0:
        raise Exception("Keine oder ungültige Daten erhalten.")
    
    df_table = pd.DataFrame(table_json)
    return df_table

if __name__ == "__main__":
    try:
        df = get_current_bundesliga_table()
        print("Aktuelle Bundesliga-Tabelle:")
        print(df)
    except Exception as e:
        print("Fehler:", e)
