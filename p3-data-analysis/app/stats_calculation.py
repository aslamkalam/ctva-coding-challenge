import logging
import pandas as pd
from database import SessionLocal
from models import WeatherStats
from config import LOG_FILE
from datetime import datetime

# Logging setup (using config)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_weather_data():
    """
    Fetches weather data from the database using pandas.

    Returns:
        pandas.DataFrame: The weather data DataFrame, or None if fetching fails.
    """

    db = SessionLocal()
    try:
        query = """
            SELECT station_id, date, max_temp, min_temp, precipitation
            FROM weather_data
        """
        df = pd.read_sql_query(query, db.bind, parse_dates=['date'])
        return df
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return None
    finally:
        db.close()


def clean_and_transform_data(df):
    """
    Cleans and transforms the weather data using pandas.

    Args:
        df (pandas.DataFrame): The weather data DataFrame.

    Returns:
        pandas.DataFrame: The cleaned and transformed DataFrame, or None if all
            records are missing.
    """

    if df is None:
        return None

    df = df.copy()  # Create a copy to avoid modifying the original DataFrame

    df.replace(-9999, pd.NA, inplace=True)
    df.dropna(inplace=True)

    if df.empty:
        logging.info("All records are missing. Skipping statistics calculation.")
        return None

    df.loc[:, 'year'] = df['date'].dt.year  # Ensure 'year' is a datetime.datetime object
    return df


def calculate_statistics(df):
    """
    Calculates weather statistics using pandas.

    Args:
        df (pandas.DataFrame): The cleaned and transformed weather data DataFrame.

    Returns:
        pandas.DataFrame: The DataFrame containing calculated statistics, or None
            if data cleaning failed.
    """

    if df is None:
        return None

    stats_df = df.groupby(['station_id', 'year']).agg(
        avg_max_temp=('max_temp', 'mean'),
        avg_min_temp=('min_temp', 'mean'),
        total_precipitation=('precipitation', 'sum')
    ).reset_index()

    # Round the calculated statistics to two decimal places
    stats_df['avg_max_temp'] = stats_df['avg_max_temp'].round(2)
    stats_df['avg_min_temp'] = stats_df['avg_min_temp'].round(2)
    stats_df['total_precipitation'] = stats_df['total_precipitation'].round(2)

    return stats_df


def store_statistics(stats_df):
    """
    Stores the calculated weather statistics in the database.

    Args:
        stats_df (pandas.DataFrame): The DataFrame containing weather statistics.
    """

    db = SessionLocal()
    try:
        stats_entries = []
        for _, row in stats_df.iterrows():
            existing_record = db.query(WeatherStats).filter(
                WeatherStats.station_id == row['station_id'],
                WeatherStats.year == row['year']
            ).first()

            if not existing_record:
                stats_entry = WeatherStats(
                    station_id=row['station_id'],
                    year=row['year'],
                    avg_max_temp=row['avg_max_temp'],
                    avg_min_temp=row['avg_min_temp'],
                    total_precipitation=row['total_precipitation']
                )
                stats_entries.append(stats_entry)

            else:
                logging.info(f"Record for station {row['station_id']} and year {row['year']} already exists. Skipping.")

        num_records_written = len(stats_entries)
        if stats_entries:
            db.bulk_save_objects(stats_entries)
            db.commit()
            logging.info(f"Calculated and stored {num_records_written} weather statistics records.")
        else:
            logging.info("No new weather statistics to calculate or store.")

    except Exception as e:
        db.rollback()
        logging.error(f"Error storing statistics: {e}")
    finally:
        db.close()


def calculate_and_store_all_stats():
    """
    Orchestrates the entire statistics calculation and storage process.
    """

    df = fetch_weather_data()

    if df is None:  # Data fetching failed, exit early
        return

    df = clean_and_transform_data(df)

    if df is None:  # Data cleaning/transformation failed
        return

    stats_df = calculate_statistics(df)

    if stats_df is None:  # Statistic calculation failed
        return

    store_statistics(stats_df)


