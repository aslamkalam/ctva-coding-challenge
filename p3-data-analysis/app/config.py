import os
from dotenv import load_dotenv

# Load environment variables from a file named ".env" located in the project root directory
load_dotenv()

# Get the database connection URL from the environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Get the log file path from the environment variable
LOG_FILE = os.environ.get("LOG_FILE")
