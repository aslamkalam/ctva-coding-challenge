import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Rest_API.app.models import WeatherStats  # Absolute import for WeatherStats model
from .conftest import client, test_db


def test_get_weather_stats_no_filter(client, test_db):
    """
    Tests the `/api/weather/stats` endpoint with no filters applied.

    This test performs the following steps:
        1. Creates two sample WeatherStats objects with different station IDs and years.
        2. Adds the sample data to the test database using the `test_db` fixture.
        3. Sends a GET request to the `/api/weather/stats` endpoint using the `client` fixture.
        4. Asserts that the response status code is 200 (success).
        5. Parses the JSON response data.
        6. Verifies that the response data contains two elements (matching the test data).
        7. Checks that the station IDs in the response data match the created test data.
    """

    # Add test data to the database
    weather_stats1 = WeatherStats(station_id="station1", year=1985, avg_max_temp=28.0, avg_min_temp=12.0, total_precipitation=60.0)
    weather_stats2 = WeatherStats(station_id="station2", year=2001, avg_max_temp=32.0, avg_min_temp=18.0, total_precipitation=80.0)

    test_db.add_all([weather_stats1, weather_stats2])
    test_db.commit()

    response = client.get("/api/weather/stats")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["station_id"] == "station1"
    assert data[1]["station_id"] == "station2"


def test_get_weather_stats_filter_by_station(client, test_db):
    """
    Tests the `/api/weather/stats` endpoint filtered by station_id.

    This test performs the following steps:
        1. Creates two sample WeatherStats objects with different station IDs and years.
        2. Adds the sample data to the test database using the `test_db` fixture.
        3. Sends a GET request to the `/api/weather/stats?station_id=station1` endpoint,
           filtering by station_id.
        4. Asserts that the response status code is 200 (success).
        5. Parses the JSON response data.
        6. Verifies that the response data contains one element (filtered data).
        7. Checks that the station ID in the response data matches the filter value.
    """

    # Add test data
    weather_stats1 = WeatherStats(station_id="station1", year=1989, avg_max_temp=28.0, avg_min_temp=12.0, total_precipitation=60.0)
    weather_stats2 = WeatherStats(station_id="station2", year=2002, avg_max_temp=32.0, avg_min_temp=18.0, total_precipitation=80.0)

    test_db.add_all([weather_stats1, weather_stats2])
    test_db.commit()

    response = client.get("/api/weather/stats?station_id=station1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["station_id"] == "station1"


def test_get_weather_stats_filter_by_year(client, test_db):
    """
    Tests the `/api/weather/stats` endpoint filtered by year.

    This test performs the following steps:
        1. Creates two sample WeatherStats objects with different station IDs and years.
        2. Adds the sample data to the test database using the `test_db` fixture.
        3. Sends a GET request to the `/api/weather/stats?year=2010` endpoint,
           filtering by year.
        4. Asserts that the response status code is 200 (success).
        5. Parses the JSON response data.
        6. Verifies that the response data contains one element (filtered data).
        7. Checks that the year in the response data matches the filter value.
    """

    # Add test data
    weather_stats1 = WeatherStats(station_id="station1", year=2012, avg_max_temp=28.0, avg_min_temp=12.0, total_precipitation=60.0)
    weather_stats2 = WeatherStats(station_id="station2", year=2010, avg_max_temp=32.0, avg_min_temp=18.0, total_precipitation=80.0)

    test_db.add_all([weather_stats1, weather_stats2])
    test_db.commit()

    response = client.get("/api/weather/stats?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["year"] == 2010