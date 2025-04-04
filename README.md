# Football Data Analysis Service

## Purpose

This service collects, processes, and analyzes football (soccer) match data from various sources. It merges CSV files with live API data, cleans and standardizes the data, computes team and player statistics (including Poisson-based goal predictions), and visualizes the results through an interactive dashboard.

## How It Works

The service follows these steps:

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
- API access credentials (e.g., for OpenLigaDB) if live data is used

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

- **API Access:**  
  Update your API keys and endpoint settings in the configuration file (if applicable).

- **CSV Data Paths:**  
  Adjust the file paths in the configuration or directly in the scripts to point to your CSV data files.

- **Logging & Environment:**  
  Ensure the logging configuration and project root structure (with proper `__init__.py` files) are set up to support relative imports.

### Step 4: Run the Service

- **Data Processing Pipeline:**  
  Run the main data processing module:
  ```bash
  python -m src.data.data_processing
  ```
  This will fetch, merge, and analyze the data.

- **Dashboard:**  
  Launch the dashboard to visualize the analysis results:
  ```bash
  python -m src.dashboard.dashboard
  ```

## Customizing the Service

- **Data Sources:**  
  Modify CSV file paths and API endpoints as needed to reflect your data environment.

- **Statistical Models:**  
  Adjust parameters in the Poisson model (and other analyses) to better suit your analytical needs.

- **Dashboard:**  
  Customize the dashboard's layout, charts, and visual settings in the `dashboard.py` module.

## Troubleshooting

- **Import Issues:**  
  Ensure every directory in the package (e.g., `src/`, `src/api/`, `src/data/`, etc.) includes an `__init__.py` file.  
  Run the project from the root directory (e.g., using `python -m src.data.data_processing`) to enable relative imports.

- **API Errors:**  
  Double-check your API credentials and endpoint configurations.

- **Data Merging Problems:**  
  Verify that CSV file formats and paths are correct and consistent with the expected structure.

- **Logging:**  
  Review the log files (e.g., `logs/data_processing.log`) for detailed error messages to help diagnose issues.

Enjoy exploring your football data and gaining actionable insights!