# Weather Data Viewer

A simple Streamlit app to view weather data from a database, with filtering options based on station, date, or year.

## Features
- Select between two tables: `weather_data` and `weather_stats`.
- Filter data by station ID, start date, end date, and year.
- If no filters are selected, view the first 100 rows from the chosen table.
- Dynamic data fetching based on the selected filters.

## Prerequisites
- Required libraries:
  - Streamlit
  - SQLAlchemy
  - Pandas
  - python-dotenv

## Run the app locally

- streamlit run weather_data_ui.py

### check UI in 8501 port
- http://localhost:8501/