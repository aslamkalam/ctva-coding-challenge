import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Absolute import for project structure
from datetime import date
from Rest_API.app.models import WeatherData  # Absolute import for WeatherData model
from .conftest import client, test_db


def test_get_weather_data_no_filter(client, test_db):
    """
    Tests the `/api/weather` endpoint with no filters applied.

    This test performs the following steps:
        1. Creates two sample WeatherData objects with different station IDs and dates.
        2. Adds the sample data to the test database using the `test_db` fixture.
        3. Sends a GET request to the `/api/weather` endpoint using the `client` fixture.
        4. Asserts that the response status code is 200 (success).
        5. Parses the JSON response data.
        6. Verifies that the response data contains two elements (matching the test data).
        7. Checks that the station IDs in the response data match the created test data.
    """

    # Add test data to the database
    weather_data1 = WeatherData(station_id="station1", date=date(2024, 1, 1), max_temp=25.0, min_temp=10.0, precipitation=5.0)
    weather_data2 = WeatherData(station_id="station2", date=date(2024, 1, 2), max_temp=30.0, min_temp=15.0, precipitation=10.0)
    test_db.add_all([weather_data1, weather_data2])
    test_db.commit()

    response = client.get("/api/weather")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["station_id"] == "station1"
    assert data[1]["station_id"] == "station2"


def test_get_weather_data_filter_by_station(client, test_db):
    """
    Tests the `/api/weather` endpoint filtered by station_id.

    This test performs the following steps:
        1. Creates two sample WeatherData objects with different station IDs and dates.
        2. Adds the sample data to the test database using the `test_db` fixture.
        3. Sends a GET request to the `/api/weather?station_id=station1` endpoint,
           filtering by station_id.
        4. Asserts that the response status code is 200 (success).
        5. Parses the JSON response data.
        6. Verifies that the response data contains one element (filtered data).
        7. Checks that the station ID in the response data matches the filter value.
    """

    # Add test data
    weather_data1 = WeatherData(station_id="station1", date=date(2024, 1, 1), max_temp=25.0, min_temp=10.0, precipitation=5.0)
    weather_data2 = WeatherData(station_id="station2", date=date(2024, 1, 2), max_temp=30.0, min_temp=15.0, precipitation=10.0)
    test_db.add_all([weather_data1, weather_data2])
    test_db.commit()

    response = client.get("/api/weather?station_id=station1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["station_id"] == "station1"


def test_get_weather_data_filter_by_date(client, test_db):
    """
    Tests the `/api/weather` endpoint filtered by date.

    This test performs the following steps:
        1. Creates two sample WeatherData objects with different station IDs and dates.
        2. Adds the sample data to the test database using the `test_db` fixture.
        3. Sends a GET request to the `/api/weather?date=2024-01-01` endpoint,
           filtering by date.
        4. Asserts that the response status code is 200 (success).
        5. Parses the JSON response data.
        6. Verifies that the response data contains one element (filtered data).
        7. Checks that the date in the response data matches the filter value.
    """

    # Add test data
    weather_data1 = WeatherData(station_id="station1", date=date(2024, 1, 1), max_temp=25.0, min_temp=10.0, precipitation=5.0)
    weather_data2 = WeatherData(station_id="station2", date=date(2024, 1, 2), max_temp=30.0, min_temp=15.0, precipitation=10.0)
    test_db.add_all([weather_data1, weather_data2])
    test_db.commit()

    response = client.get("/api/weather?date=2024-01-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["date"] == "2024-01-01"