### Weather Data Ingestion

This project automates the ingestion of weather data from text files into a database.

#### Prerequisites:

PostgreSQL: Install and configure PostgreSQL on your system.

#### Configuration:

Create a PostgreSQL Database:

Create a new database user with appropriate privileges.

Create a new database for the weather data.

Create .env file:

Create a file named .env in the project root directory.

Add the following lines to the .env file:
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
DATA_DIRECTORY=./data/wx_data 
LOG_FILE=weather_data_ingestion.log 

Replace <username>, <password>, <host>, <port>, and <database_name> with your actual PostgreSQL database credentials.

#### Installation:

Create a virtual environment (recommended):

Bash

python -m venv venv

source venv/bin/activate  # For Linux/macOS

venv\Scripts\activate.bat  # For Windows

Install required libraries:

Bash

pip install -r requirements.txt

#### Configuration:

Create a .env file  to store sensitive information like database credentials.
Update config.py with your database connection details and file paths.

#### Running the Ingestion Process:

Ensure your weather data files are placed in the data/wx_data/ directory.
Run the main script:
Bash

python main.py
This will process the weather data files, ingest the data into the database, and log messages about the process.

### Additional Notes:

The models.py file defines the data models for weather data in the database.
The ingestion.py file contains functions for processing the weather data files (e.g., rounding temperatures, handling missing values) before ingesting them.
The weather_data_ingestion.log file records messages about the ingestion process, such as start time, completion time, and number of records ingested.