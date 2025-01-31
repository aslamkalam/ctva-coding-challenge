from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, UniqueConstraint, DateTime, func, Index

Base = declarative_base()
class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    max_temp = Column(Float, nullable=True)  # Maximum temperature (tenths of a degree Celsius)
    min_temp = Column(Float, nullable=True)  # Minimum temperature (tenths of a degree Celsius)
    precipitation = Column(Float, nullable=True)  # Precipitation (tenths of a millimeter)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())  # Add created_at for record creation timestamp

    # Enforce unique constraint on station_id and date combination
    __table_args__ = (
        UniqueConstraint('station_id', 'date', name='_station_date_uc'),
        Index('idx_station_date', 'station_id', 'date'))  # Add index for faster queries on station_id and date
