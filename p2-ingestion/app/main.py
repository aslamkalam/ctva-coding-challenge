from datetime import datetime
import logging

# Import database components
from database import Base, engine

# Import functions from ingestion module
from ingestion import process_all_files

# Import configuration
from config import LOG_FILE

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    """
    The main function that orchestrates the weather data ingestion process.

    It logs the start time, calls the `process_all_files` function to ingest data,
    logs the end time, total ingestion time, and total number of records ingested.
    """

    start_time = datetime.now()
    logging.info(f"Weather data ingestion started at {start_time}")

    total_records_ingested = process_all_files()  # Call the function to ingest data

    end_time = datetime.now()
    total_ingestion_time = end_time - start_time

    logging.info(f"Weather data ingestion finished at {end_time}")
    logging.info(f"Total ingestion time: {total_ingestion_time}")
    logging.info(f"Total records ingested: {total_records_ingested}")


if __name__ == "__main__":
    main()