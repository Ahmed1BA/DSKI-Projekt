BAYERN = "bayern münchen"

TEAM_MAPPING = {
    "bayern munich": BAYERN,
    "bayern münchen": BAYERN,
    "fc bayern": BAYERN,
    "hertha bsc": "hertha bsc",
    "sc freiburg": "sc freiburg",
    "vfl wolfsburg": "vfl wolfsburg",
    "borussia mönchengladbach": "borussia mönchengladbach",
    "fsv mainz 05": "fsv mainz 05",
    "borussia dortmund": "borussia dortmund",
    "1899 hoffenheim": "1899 hoffenheim",
    "bayer leverkusen": "bayer leverkusen",
    "eintracht frankfurt": "eintracht frankfurt",
    "fc augsburg": "fc augsburg",
    "vfb stuttgart": "vfb stuttgart",
    "rb leipzig": "rb leipzig",
    "hamburger sv": "hamburger sv",
    "vfl bochum": "vfl bochum",
    "spvgg greuther fürth": "spvgg greuther fürth",
    "union berlin": "union berlin",
    "arminia bielefeld": "arminia bielefeld",
    "1.fc köln": "1.fc köln"
}


def standardize_team(name: str) -> str:
    if not isinstance(name, str):
        return name
    name_clean = name.lower().strip()
    return TEAM_MAPPING.get(name_clean, name_clean)
