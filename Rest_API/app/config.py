import os
from dotenv import load_dotenv

# Explicitly specify the path to the .env file
# This is crucial if the .env file is not located in the same directory as this script.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Get the DATABASE_URL from the loaded environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")