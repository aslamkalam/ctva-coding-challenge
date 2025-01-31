from pydantic import BaseModel
from pydantic.types import date
from typing import Optional
from pydantic import ConfigDict

class WeatherDataSchema(BaseModel):
    """
    Pydantic schema for validating and representing WeatherData objects.

    Attributes:
        station_id (str): Unique identifier for the weather station.
        date (date): Date for which the weather data is recorded.
        max_temp (Optional[float]): Maximum temperature (optional, can be None).
        min_temp (Optional[float]): Minimum temperature (optional, can be None).
        precipitation (Optional[float]): Precipitation (optional, can be None).
    """
    station_id: str
    date: date
    max_temp: Optional[float] = None
    min_temp: Optional[float] = None
    precipitation: Optional[float] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Uncomment this if you want to create instances from existing objects
    # class Config:
    #     from_attributes = True


class WeatherStatsSchema(BaseModel):
    """
    Pydantic schema for validating and representing WeatherStats objects.

    Attributes:
        station_id (str): Unique identifier for the weather station.
        year (int): Year for which the statistics are calculated.
        avg_max_temp (Optional[float]): Average maximum temperature (optional, can be None).
        avg_min_temp (Optional[float]): Average minimum temperature (optional, can be None).
        total_precipitation (Optional[float]): Total precipitation (optional, can be None).
    """
    station_id: str
    year: int
    avg_max_temp: Optional[float] = None
    avg_min_temp: Optional[float] = None
    total_precipitation: Optional[float] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Uncomment this if you want to create instances from existing objects
    # class Config:
    #     from_attributes = True