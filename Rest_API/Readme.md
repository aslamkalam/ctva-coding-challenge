### Weather Data API

This project provides a RESTful API for managing weather data, including:

Retrieving weather data for specific stations or dates
Obtaining weather statistics (average max/min temperature, total precipitation)

Prerequisites

Python 3.11

pip package manager

### Installation

Create a virtual environment (recommended):

Bash

python -m venv .venv
 
Windows:.venv\Scripts\activate.bat

Install dependencies:
Bash

pip install requirements.txt

### Running the API

Configure database connection:
Update the database connection details in Rest_API/app/config.py to match your PostgreSQL setup (host, port, database name, username, password).

Start the API server:

Bash

uvicorn Rest_API.app.main:app

This will start the API server on http://localhost:8000 by default.

### API Endpoints

#### Weather Data

#### GET /api/weather

Retrieves all weather data.

#### Optional query parameters:
station_id: Filter by station ID.

date: Filter by date (format: YYYY-MM-DD).

#### GET /api/weather/stats

Retrieves weather statistics (average max/min temperature, total precipitation).

#### Optional query parameters:

station_id: Filter by station ID.

year: Filter by year.

### Running Tests

Navigate to the project root directory.

#### Run tests:
Bash

pytest -v

#### Database

The API uses a PostgreSQL database to store weather data and statistics. You'll need to configure the connection details in Rest_API/app/config.py.

#### Ingestion and Data Analysis

The API retrieves pre-processed weather data from the PostgreSQL database.