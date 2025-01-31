"""
This module handles the ingestion of weather data from text files into the database.

It reads weather data from files in the specified data directory, 
processes the data, and inserts it into the database.
"""

import os
import logging
import pandas as pd
import numpy as np
from tqdm import tqdm
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from models import WeatherData  # Make sure this import is correct
from config import DATA_DIRECTORY, LOG_FILE  # Make sure this import is correct

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def ingest_weather_data(df: pd.DataFrame) -> int:
    """
    Ingests weather data from a Pandas DataFrame into the database.

    Args:
        df (pd.DataFrame): A Pandas DataFrame containing weather data.

    Returns:
        int: The number of records ingested into the database.
    """

    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            existing_record = db.query(WeatherData).filter(
                WeatherData.station_id == row["station_id"],
                WeatherData.date == row["date"],
            ).first()

            if not existing_record:
                weather_data_entry = WeatherData(**row)
                db.add(weather_data_entry)

        db.commit()
        print(f"Records ingested: {len(df)}")  # Confirmation message
        return len(df)

    except IntegrityError as e:
        db.rollback()
        logging.error(f"Duplicate record found: {e}")
        return 0

    except Exception as e:
        db.rollback()
        logging.error(f"Error during ingestion: {e}")
        return 0

    finally:
        db.close()


def process_weather_file(file_path: str, station_id: str) -> int:
    """
    Processes a single weather data file, rounding floats and handling NaN/inf.

    Args:
        file_path (str): The path to the weather data file.
        station_id (str): The station ID for the data in the file.

    Returns:
        int: The number of records ingested from the file.
    """

    try:
        df = pd.read_csv(
            file_path, sep="\t", header=None, names=["date", "max_temp", "min_temp", "precipitation"], na_values=-9999
        )
        df["station_id"] = station_id
        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d").dt.date

        # Round floats and handle NaN/inf (Corrected)
        df["max_temp"] = df["max_temp"].apply(
            lambda x: round(x / 10.0, 6) if pd.notna(x) and not np.isinf(x) else None
        )
        df["min_temp"] = df["min_temp"].apply(
            lambda x: round(x / 10.0, 6) if pd.notna(x) and not np.isinf(x) else None
        )
        df["precipitation"] = df["precipitation"].apply(
            lambda x: round(x / 10.0, 6) if pd.notna(x) and not np.isinf(x) else None
        )

        # print("DataFrame after processing:", df)  # Debugging print statement

        return ingest_weather_data(df)

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return 0

    except pd.errors.ParserError as pe:
        logging.error(f"Error parsing file: {pe}")
        return 0

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return 0


def process_all_files():
    """
    Processes all weather data files in the data directory.

    Returns:
        int: The total number of records ingested from all files.
    """

    total_files = len([f for f in os.listdir(DATA_DIRECTORY) if f.endswith(".txt")])
    total_records_ingested = 0

    with tqdm(total=total_files, desc="Processing Weather Files") as pbar:
        for filename in os.listdir(DATA_DIRECTORY):
            if filename.endswith(".txt"):
                file_path = os.path.join(DATA_DIRECTORY, filename)
                station_id = filename[:-4]

                logging.info(f"Processing file: {filename} started.")

                records_ingested = process_weather_file(file_path, station_id)
                total_records_ingested += records_ingested

                logging.info(f"Finished processing file: {filename}.")
                logging.info(f"Records ingested from {filename}: {records_ingested}")
                pbar.update(1)

    return total_records_ingested