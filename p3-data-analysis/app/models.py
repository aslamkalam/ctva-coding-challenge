from sqlalchemy import Column, Integer, String, Float, UniqueConstraint, Index
from database import Base

class WeatherStats(Base):
    """
    This class defines the WeatherStats model for storing aggregated
    weather statistics for each station and year.

    Attributes:
        id (int): Unique identifier (primary key, auto-incrementing).
        station_id (str): Station ID (not nullable).
        year (int): Year for which the statistics are calculated (not nullable).
        avg_max_temp (float): Average maximum temperature for the year (nullable).
        avg_min_temp (float): Average minimum temperature for the year (nullable).
        total_precipitation (float): Total precipitation for the year (nullable).
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
        Index('idx_station_year', 'station_id', 'year')  # Composite index for faster queries
    )