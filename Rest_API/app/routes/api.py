from typing import List, Optional
from datetime import  date  # Import date
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..utils import convert_float  # Import the convert_float function
from ..database import get_db  # Import the get_db dependency
from ..models import WeatherData, WeatherStats  # Import database models
from ..schemas import WeatherDataSchema, WeatherStatsSchema  # Import Pydantic schemas

router = APIRouter()

ITEMS_PER_PAGE = 10

@router.get("/api/weather", response_model=List[WeatherDataSchema], tags=["Weather Data"])
async def get_weather_data(
    db: Session = Depends(get_db),  # Get database session from dependency
    station_id: Optional[str] = Query(None, description="Filter by station ID"),
    date: Optional[date] = Query(None, description="Filter by date (YYYY-MM-DD)", examples={"default": "2024-01-01"}),
    page: int = Query(1, description="Page number, default is 1"),
):
    """
    Retrieves weather data based on optional filters and pagination.

    Args:
        db: Database session (obtained through dependency).
        station_id: Optional filter by station ID.
        date: Optional filter by date (YYYY-MM-DD format).
        page: Page number for pagination (default: 1).

    Returns:
        A list of weather data objects (validated using WeatherDataSchema).

    Raises:
        HTTPException: 404 Not Found if the requested page is out of bounds.
    """

    query = db.query(WeatherData)  # Start building the query

    # Apply filters if provided
    if station_id:
        query = query.filter(WeatherData.station_id == station_id)

    if date:
        query = query.filter(WeatherData.date == date)  # Direct date comparison

    # Get total count of matching records
    total_count = query.count()

    # Calculate offset for pagination
    offset = (page - 1) * ITEMS_PER_PAGE

    # Handle invalid page requests (out of bounds)
    if offset >= total_count and total_count > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    # Apply pagination (offset and limit)
    weather_data = query.offset(offset).limit(ITEMS_PER_PAGE).all()

    # Apply precision handling to temperature and precipitation values
    for item in weather_data:
        item.max_temp = convert_float(item.max_temp)
        item.min_temp = convert_float(item.min_temp)
        item.precipitation = convert_float(item.precipitation)

    # Return the list of weather data (validated with schema)
    return weather_data


@router.get("/api/weather/stats", response_model=List[WeatherStatsSchema], tags=["Weather Statistics"])
async def get_weather_stats(
    db: Session = Depends(get_db),
    station_id: Optional[str] = Query(None, description="Filter by station ID"),
    year: Optional[int] = Query(None, description="Filter by year"),
    page: int = Query(1, description="Page number, default is 1"),
):
    """
    Retrieves weather statistics based on optional filters and pagination.

    Args:
        db: Database session (obtained through dependency).
        station_id: Optional filter by station ID.
        year: Optional filter by year.
        page: Page number for pagination (default: 1).

    Returns:
        A list of weather statistics objects (validated using WeatherStatsSchema).

    Raises:
        HTTPException: 404 Not Found if the requested page is out of bounds.
    """

    query = db.query(WeatherStats)  # Start building the query

    # Apply filters if provided
    if station_id:
        query = query.filter(WeatherStats.station_id == station_id)

    if year:
        query = query.filter(WeatherStats.year == year)

    # Get total count of matching records
    total_count = query.count()

    # Calculate offset for pagination
    offset = (page - 1) * ITEMS_PER_PAGE

    # Handle invalid page requests (out of bounds)
    if offset >= total_count and total_count > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    # Apply pagination (offset and limit)
    weather_stats = query.offset(offset).limit(ITEMS_PER_PAGE).all()

    # Apply precision handling to temperature and precipitation values
    for item in weather_stats:
        item.avg_max_temp = convert_float(item.avg_max_temp)
        item.avg_min_temp = convert_float(item.avg_min_temp)
        item.total_precipitation = convert_float(item.total_precipitation)

    # Return the list of weather statistics
    return weather_stats