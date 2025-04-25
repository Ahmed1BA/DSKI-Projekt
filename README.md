# Football Data Analysis Service

## Purpose

This service collects, processes, and analyzes football (soccer) match data from various sources. It merges CSV files with live API data, cleans and standardizes the data, computes team and player statistics (including Poisson-based goal predictions), and visualizes the results through an interactive dashboard.

## How It Works

- **Data Retrieval:**  
  Fetches live league data via API and loads historical data from CSV files.

- **Data Processing:**  
  Merges, cleans, and standardizes datasets by unifying column names and mapping team names across sources.

- **Statistical Analysis:**  
  Computes team statistics (wins, draws, losses, goals, etc.), player performance metrics, and uses Poisson models for goal prediction.

- **Visualization:**  
  Displays the processed data and analysis results using an interactive dashboard for easy interpretation.

## Components

- **API Client:**  
  Handles external API requests (e.g., retrieving current league tables from OpenLigaDB).

- **Data Processing Modules:**  
  Modules such as `merge_data.py`, `data_processing.py`, and `csv_analysis.py` work together to clean and merge data.

- **Statistical Models:**  
  Implements statistical analysis including Poisson-based predictions for match outcomes.

- **Team Mapping:**  
  Standardizes team names to ensure consistency across various data sources.

- **Dashboard:**  
  Provides a user-friendly interface for visualizing the results of the data analysis.

## Setup Guide

### Prerequisites

- Python 3.8+
- Required Python packages (see `requirements.txt`)
- API access credentials (e.g., for OpenLigaDB or API-Sports) if live data is used

### Step 1: Clone the Repository

```bash
git clone https://github.com/Ahmed1BA/DSKI-Projekt
cd DSKI-Projekt
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure the Project

- **CSV Data Paths:**  
  Adjust the file paths in the configuration or directly in the scripts to point to your CSV data files.

- **Logging & Environment:**  
  Ensure the logging configuration and project root structure (with proper `__init__.py` files) are set up to support relative imports.

### Step 4: API-Key-Hinweis

Manchmal schlägt die API-Abfrage fehl, wenn derselbe API-Key von verschiedenen IP-Adressen aus genutzt wird. Um solche Fehler zu vermeiden, erstelle dir bitte einen eigenen API-Key unter:

- https://api-sports.io

Trage den erhaltenen Key in die Datei `src/api_key.py` ein:

```python
# src/api_key.py
API_KEY = "DEIN_API_KEY"
```

Alternativ kannst du den Key auch als Umgebungsvariable `API_KEY` setzen und in deinen Modulen darauf zugreifen.

### Step 5: Run the Service

- **Data Processing Pipeline:**  
  ```bash
  python -m src.data.data_processing
  ```
  Dies ruft Daten ab, merged sie und erstellt die Analyse.

- **Dashboard:**  
  ```bash
  python -m src.dashboard.dashboard
  ```

## Customizing the Service

- **Data Sources:**  
  Modifiziere CSV-Dateipfade und API-Endpunkte nach Bedarf.

- **Statistical Models:**  
  Passe Parameter des Poisson-Modells (und andere Analysen) an.

- **Dashboard:**  
  Gestalte Layout, Charts und visuelle Einstellungen in `dashboard.py` um.

## Troubleshooting

- **Import Issues:**  
  Überprüfe, dass alle Verzeichnisse (`src/`, `src/api/`, `src/data/`, etc.) ein `__init__.py` besitzen und führe das Projekt aus dem Root-Verzeichnis aus.

- **API Errors:**  
  Bei Fehlern überprüfe deinen API-Key, den Header (`x-apisports-key`) und die Dokumentation unter [API Sports](https://api-sports.io).

- **Data Merging Problems:**  
  Kontrolliere, ob die CSV-Formate und -Pfade korrekt sind.

- **Logging:**  
  Schau in die Logdateien (z.B. `logs/data_processing.log`), um detaillierte Fehlermeldungen zu sehen.

Enjoy exploring your football data and gaining actionable insights!

