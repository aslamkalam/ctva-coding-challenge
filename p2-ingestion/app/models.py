from sqlalchemy import Column, Integer, String, Date, Float, UniqueConstraint, DateTime, func, Index

# Import Base class from database.py
from database import Base


class WeatherData(Base):
    """
    This class defines the WeatherData model for storing weather data in the database.

    It includes columns for station ID, date, maximum temperature, minimum temperature,
    precipitation, and a timestamp for record creation. It also enforces a unique constraint
    on the combination of station ID and date to prevent duplicate entries.
    """

    __tablename__ = "weather_data"  # Table name in the database

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier (auto-incrementing)
    station_id = Column(String, nullable=False)  # Station ID (not nullable)
    date = Column(Date, nullable=False)  # Date (not nullable)
    max_temp = Column(Float, nullable=True)  # Maximum temperature (tenths of a degree Celsius)
    min_temp = Column(Float, nullable=True)  # Minimum temperature (tenths of a degree Celsius)
    precipitation = Column(Float, nullable=True)  # Precipitation (tenths of a millimeter)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # Timestamp for record creation (automatically set on insert)

    # Enforce unique constraint on station_id and date combination
    __table_args__ = (
        UniqueConstraint("station_id", "date", name="_station_date_uc"),
        Index("idx_station_date", "station_id", "date"),  # Index for faster queries
    )