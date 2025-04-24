from google.generativeai import configure, GenerativeModel


from src.analysis.poisson import get_poisson_matrix_for_gemini
from src.data.data_processing import run_data_processing_pipeline
from src.mapping.team_mapping import standardize_team

api_key = "AIzaSyAUx3WY2bgMfR3etBOkMbD6lyR_7D_pN4w"

configure(api_key=api_key)


def generate_game_forecast(team1: str, team2: str) -> str:
    team1_std = standardize_team(team1)
    team2_std = standardize_team(team2)

    print(f"Gemini aufgerufen mit: {team1_std} vs {team2_std}")

    team_data, player_data, match_data, _ = run_data_processing_pipeline()

    if match_data is None or match_data.empty:
        raise ValueError(
            "match_data ist leer – bitte prüfe, ob deine CSV-Dateien korrekt geladen und gemerged wurden.")

    if "team" not in match_data.columns and "home_team" in match_data.columns:
        match_data["team"] = match_data["home_team"].apply(standardize_team)
        print("team-Spalte wurde aus 'home_team' erstellt.")

    print(f"Spalten in match_data: {match_data.columns.tolist()}")
    print(
        f"Teams in match_data: {match_data['team'].unique() if 'team' in match_data.columns else 'Keine team-Spalte'}")

    prob_matrix = get_poisson_matrix_for_gemini(team1_std, team2_std, match_data)

    top_probs = prob_matrix.stack().sort_values(ascending=False).head(3)
    prob_summary = "\n".join([f"{score[0]}:{score[1]} → {round(prob * 100, 1)}%" for score, prob in top_probs.items()])

    prompt = f"""
    Erstelle eine Spielvorhersage für das Bundesliga-Spiel zwischen {team1} und {team2}.

    Die wahrscheinlichsten Ergebnisse laut Poisson-Modell sind:
    {prob_summary}

    Bewerte realistisch, welches Team Vorteile hat, welche Spielverläufe denkbar sind
    und wie wahrscheinlich ein Unentschieden ist. Formuliere es wie ein kurzer
    Sportkommentar oder Spielbericht.
    """

    model = GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    return response.text


if __name__ == "__main__":
    forecast = generate_game_forecast("bayern munich", "hamburger sv")
    print("Gemini-Vorhersage:")
    print(forecast)