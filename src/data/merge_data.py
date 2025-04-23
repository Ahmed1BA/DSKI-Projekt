import os
import logging
import pandas as pd

from ..api.api_client import ApiSportsClient
from ..mapping.team_mapping import standardize_team
from ..analysis.csv_analysis import load_csv_data


def load_fixtures_to_df(api_key, league_id, season, data_dir="data") -> pd.DataFrame:
    client = ApiSportsClient(api_key, data_dir=data_dir)
    data = client.get_fixtures(league_id, season)

    if not data:
        logging.warning("Keine Daten von der API erhalten.")
        return pd.DataFrame()

    fixtures = data.get("response", [])
    if not fixtures:
        logging.warning("Keine Fixture-Daten in der API Response gefunden.")

    df = pd.json_normalize(fixtures)

    if "teams.home.name" in df.columns and "teams.away.name" in df.columns:
        df["home_team_std"] = df["teams.home.name"].apply(standardize_team)
        df["away_team_std"] = df["teams.away.name"].apply(standardize_team)
    else:
        logging.warning(
    "Erwartete Spalten in API-Daten fehlen: "
    "'teams.home.name' oder 'teams.away.name'"
    )


    logging.info("API-Fixture-Daten geladen: %d Zeilen", df.shape[0])
    logging.debug("API DataFrame Vorschau:\n%s", df.head())
    return df


def merge_api_csv(api_key, league_id, season, csv_path) -> pd.DataFrame:
    df_api = load_fixtures_to_df(api_key, league_id, season)
    df_csv = load_csv_data(csv_path, team_col="team_title")

    logging.info("API-Daten Shape: %s | CSV-Daten Shape: %s", df_api.shape, df_csv.shape)
    logging.debug("API DataFrame head:\n%s", df_api.head())
    logging.debug("CSV DataFrame head:\n%s", df_csv.head())

    if df_api.empty or df_csv.empty:
        logging.warning("Eines der DataFrames ist leer. Merge wird abgebrochen.")
        return pd.DataFrame()

    if "team_name_std" not in df_csv.columns and "team_title" in df_csv.columns:
        df_csv["team_name_std"] = df_csv["team_title"].apply(standardize_team)
        logging.info("Spalte 'team_name_std' in CSV-Daten erzeugt.")

    merged = df_api.merge(
        df_csv,
        left_on="home_team_std",
        right_on="team_name_std",
        how="inner"
    )

    logging.info("Merge erfolgreich: %d Zeilen", merged.shape[0])
    logging.debug("Merged DataFrame head:\n%s", merged.head())
    return merged


if __name__ == "__main__":
    from ..logging_config import setup_logging
    setup_logging("logs/merge_data.log")

    logging.info("Ausführen von merge_api_csv")
    KEY = "9cc1ae42d0e8531f9c57eaac6c5a0b6d"
    script_dir = os.path.dirname(__file__)
    csv_file = os.path.join(script_dir, "../../docs/filtercsv/filtered_TeamsData.csv")

    df_merged_api = merge_api_csv(KEY, 78, 2022, csv_file)

    logging.info("Merged API/CSV Shape: %s", df_merged_api.shape)
    logging.debug("Spalten: %s", df_merged_api.columns.tolist())
    logging.debug("Vorschau:\n%s", df_merged_api.head())
