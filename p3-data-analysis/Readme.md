### Weather Data Statistics Calculation

This project automates the calculation and storage of weather statistics from a database. 
It retrieves weather data for each station and year, calculates average maximum temperature, average minimum temperature, and total precipitation, and then stores these statistics in a database table.

### Installation:

Create a virtual environment (recommended):

Bash

python -m venv venv

source venv/bin/activate  # For Linux/macOS

venv\Scripts\activate.bat  # For Windows

Install required libraries:
Bash

pip install -r requirements.txt
### Configuration :

Create a .env file in the project root directory (if using environment variables).

Add the following lines to the .env file, replacing placeholders with your actual credentials:

DATABASE_URL=postgresql://username:password@host:port/database_name

LOG_FILE=weather_data_stats.log


### Running the Statistics Calculation:

Ensure your database is configured and the weather_data table exists with relevant weather data columns.

### Run the script:

Bash

python main.py
This will perform the following steps:

Fetch weather data from the database.
Clean and transform the data (handle missing values, create a 'year' column).
Calculate statistics for each station and year (average max/min temp, total precipitation).
Store the calculated statistics in the weather_stats table.
Log informative messages about the process (start/end time, number of records processed/stored).