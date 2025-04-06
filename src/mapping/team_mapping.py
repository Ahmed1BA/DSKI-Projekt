BAYERN = "Bayern München"
HOFFENHEIM = "1899 Hoffenheim"
MAINZ = "FSV Mainz 05"
UNION = "Union Berlin"

TEAM_MAPPING = {
    "bayern munich": BAYERN,
    "bayern münchen": BAYERN,
    "fc bayern": BAYERN,
    "fc bayern münchen": BAYERN,
    "hertha bsc": "Hertha BSC",
    "sc freiburg": "SC Freiburg",
    "vfl wolfsburg": "VfL Wolfsburg",
    "borussia mönchengladbach": "Borussia Mönchengladbach",
    "fsv mainz 05": MAINZ,
    "1. fsv mainz 05": MAINZ,
    "borussia dortmund": "Borussia Dortmund",
    "1899 hoffenheim": HOFFENHEIM,
    "tsg 1899 hoffenheim": HOFFENHEIM,
    "bayer leverkusen": "Bayer 04 Leverkusen",
    "eintracht frankfurt": "Eintracht Frankfurt",
    "fc augsburg": "FC Augsburg",
    "vfb stuttgart": "VfB Stuttgart",
    "rb leipzig": "Rb Leipzig",
    "hamburger sv": "Hamburger SV",
    "vfl bochum": "VfL Bochum",
    "spvgg greuther fürth": "Spvgg Greuther Fürth",
    "union berlin": UNION,
    "1. fc union berlin": UNION,
    "arminia bielefeld": "Arminia Bielefeld",
    "1. fc heidenheim 1846": "1. FC Heidenheim 1846",
    "holstein kiel": "Holstein Kiel",
    "werder bremen": "Werder Bremen",
    "fc st. pauli": "FC St. Pauli",
    "1.fc köln": "1.FC Köln"
}


def standardize_team(name: str) -> str:
    if not isinstance(name, str):
        return name
    name_clean = name.lower().strip()
    return TEAM_MAPPING.get(name_clean, name_clean)
