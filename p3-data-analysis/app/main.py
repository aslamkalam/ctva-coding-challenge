from datetime import datetime
import logging
from database import Base, engine
from stats_calculation import calculate_and_store_all_stats  # Import the function
from config import LOG_FILE

# Create tables in the database if they don't already exist
Base.metadata.create_all(bind=engine)

# Configure logging to write info messages to the specified log file
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """
    This function orchestrates the weather data statistics calculation process.

    Steps:
        1. Logs the start time of the process.
        2. Calls the `calculate_and_store_all_stats` function to calculate and store all weather statistics.
        3. Logs the end time of the process and total execution time.
    """

    start_time = datetime.now()
    logging.info(f"Statistics calculation started at {start_time}")

    calculate_and_store_all_stats()  # Calculate and store all stats at once

    end_time = datetime.now()
    logging.info(f"Statistics calculation finished at {end_time}")
    logging.info(f"Total time taken: {end_time - start_time}")


if __name__ == "__main__":
    main()