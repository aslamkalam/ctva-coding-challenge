from sqlalchemy import (Column, Integer, String, Float, UniqueConstraint,
                        Index, Date, DateTime, func)
from .database import Base

class WeatherData(Base):
    """
    This class defines the 'weather_data' table in the database,
    representing individual weather data points.

    Attributes:
        id (Integer): Unique identifier for each weather data record
            (primary key, auto-incrementing).
        station_id (String): Unique identifier for the weather station
            (not null).
        date (Date): Date for which the weather data is recorded (not null).
        max_temp (Float): Maximum temperature for the day (nullable).
        min_temp (Float): Minimum temperature for the day (nullable).
        precipitation (Float): Total precipitation for the day (nullable).
        created_at (DateTime): Timestamp of when the record was created
            (automatically set to current time with timezone).
    """

    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    max_temp = Column(Float, nullable=True)
    min_temp = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('station_id', 'date', name='_station_date_uc'),
        Index('idx_station_date', 'station_id', 'date')
    )


class WeatherStats(Base):
    """
    This class defines the 'weather_stats' table in the database,
    representing calculated weather statistics for each station and year.

    Attributes:
        id (Integer): Unique identifier for each weather statistics record
            (primary key, auto-incrementing).
        station_id (String): Unique identifier for the weather station
            (not null).
        year (Integer): Year for which the weather statistics are calculated
            (not null).
        avg_max_temp (Float): Average maximum temperature for the year (nullable).
        avg_min_temp (Float): Average minimum temperature for the year (nullable).
        total_precipitation (Float): Total precipitation for the year (nullable).
    """

    __tablename__ = 'weather_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    avg_max_temp = Column(Float, nullable=True)
    avg_min_temp = Column(Float, nullable=True)
    total_precipitation = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint('station_id', 'year', name='_station_year_uc'),
        Index('idx_station_year', 'station_id', 'year')
    )