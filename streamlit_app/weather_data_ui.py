import os
import datetime
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

st.title("Weather Data Viewer")

# Sidebar Filters
st.sidebar.header("Filters")

# Table selection
table_choice = st.sidebar.selectbox("Choose Table", ["weather_data", "weather_stats"])

# Fetch unique station IDs
@st.cache_data
def get_station_ids():
    query = "SELECT DISTINCT station_id FROM weather_data"
    df = pd.read_sql(query, engine)
    return df["station_id"].tolist()

# Fetch available years
@st.cache_data
def get_available_years():
    query = "SELECT DISTINCT year FROM weather_stats ORDER BY year"
    df = pd.read_sql(query, engine)
    return df["year"].tolist()

# Dropdown for station_id with manual entry option
station_ids = get_station_ids()
station_id = st.sidebar.selectbox("Select Station ID", [""] + station_ids)
custom_station_id = st.sidebar.text_input("Or Enter Station ID Manually")
station_id = custom_station_id if custom_station_id else station_id

# Optional Date Filters
start_date = None
end_date = None
year = None

if table_choice == "weather_data":
    start_date = st.sidebar.date_input("Start Date (YYYY-MM-DD)", None)
    end_date = st.sidebar.date_input("End Date (YYYY-MM-DD)", None)
elif table_choice == "weather_stats":
    available_years = get_available_years()
    year = st.sidebar.selectbox("Year", [""] + available_years)

# Query functions
def fetch_weather_data(station_id, start_date, end_date):
    query = "SELECT * FROM weather_data WHERE 1=1"
    params = {}

    if station_id:
        query += " AND station_id = %(station_id)s"
        params["station_id"] = station_id
    if start_date:
        query += " AND date >= %(start_date)s"
        params["start_date"] = start_date
    if end_date:
        query += " AND date <= %(end_date)s"
        params["end_date"] = end_date

    return pd.read_sql(query, engine, params=params)

def fetch_weather_stats(station_id, year):
    query = "SELECT * FROM weather_stats WHERE 1=1"
    params = {}

    if station_id:
        query += " AND station_id = %(station_id)s"
        params["station_id"] = station_id
    if year:
        query += " AND year = %(year)s"
        params["year"] = year

    return pd.read_sql(query, engine, params=params)

# Default fetch (100 rows if no filter applied)
def fetch_default_data(table_choice):
    if table_choice == "weather_data":
        query = "SELECT * FROM weather_data LIMIT 100"
    else:
        query = "SELECT * FROM weather_stats LIMIT 100"
    return pd.read_sql(query, engine)

# Fetch data on button click
if st.sidebar.button("Fetch Data"):
    if table_choice == "weather_data":
        if station_id or start_date or end_date:
            df = fetch_weather_data(station_id, start_date, end_date)
        else:
            df = fetch_default_data(table_choice)
    else:
        if station_id or year:
            df = fetch_weather_stats(station_id, year)
        else:
            df = fetch_default_data(table_choice)

    st.dataframe(df)
