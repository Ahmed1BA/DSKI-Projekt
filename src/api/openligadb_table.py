import logging
import requests
import pandas as pd



def get_current_bundesliga_table(league="bl1", season="2024") -> pd.DataFrame:
    url = f"https://www.openligadb.de/api/getbltable/{league}/{season}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Fehler beim Abrufen der Tabelle von OpenLigaDB: %s", e)
        raise

    table_json = response.json()
    if not isinstance(table_json, list) or not table_json:
        logging.error("Antwort von OpenLigaDB ist leer oder ungültig.")
        raise ValueError("Keine oder ungültige Daten erhalten.")

    df_table = pd.DataFrame(table_json)
    logging.info("Bundesliga-Tabelle erfolgreich geladen, %d Einträge", len(df_table))
    return df_table


if __name__ == "__main__":
    from ..logging_config import setup_logging
    setup_logging("logs/openligadb_table.log")

    try:
        df = get_current_bundesliga_table()
        logging.info("Tabelle geladen:\n%s", df.head())
    except Exception as e:
        logging.error("Fehler beim Laden der Bundesliga-Tabelle: %s", e)


