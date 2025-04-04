from src.mapping.team_mapping import standardize_team, BAYERN

def test_standardize_known_team():
    assert standardize_team("FC Bayern") == BAYERN
    assert standardize_team("bayern munich") == BAYERN
    assert standardize_team("  bayern münchen ") == BAYERN

def test_standardize_unknown_team():
    assert standardize_team("Karlsruher SC") == "karlsruher sc"

def test_standardize_non_string():
    assert standardize_team(None) is None
    assert standardize_team(42) == 42
