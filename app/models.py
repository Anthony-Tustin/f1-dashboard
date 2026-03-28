from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Date, Text, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base

class Driver(Base):
    __tablename__ = "drivers"

    # Primary key, uniquely (no duplictes) identifies each driver
    driver_id = Column(String, primary_key=True)
    code = Column(String(3))           # e.g. "VER"
    full_name = Column(String)
    team_name = Column(String)
    nationality = Column(String)
    permanent_number = Column(Integer)

class Constructor(Base):
    __tablename__ = "constructors"

    constructor_id = Column(String, primary_key=True)
    name = Column(String)
    nationality = Column(String)

class DriverStanding(Base):
    __tablename__ = "driver_standings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String, ForeignKey("drivers.driver_id")) #references the drivers table, drivers_id Column
    season = Column(Integer)
    position = Column(Integer)
    points = Column(Float)
    wins = Column(Integer)
    fetched_at = Column(DateTime, default=func.now()) #Automatically sets this to the current timestamp

    __table_args__ = (
        UniqueConstraint("driver_id", "season", name="uq_driver_season"),
    )

class ConstructorStanding(Base):
    __tablename__ = "constructor_standings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    constructor_id = Column(String, ForeignKey("constructors.constructor_id")) #References the constructors table, constructors_id column
    season = Column(Integer)
    position = Column(Integer)
    points = Column(Float)
    wins = Column(Integer)
    fetched_at = Column(DateTime, default=func.now())

    __table_args__ = (
        UniqueConstraint("constructor_id", "season", name="uq_constructor_season"),
    )

class RaceResult(Base):
    __tablename__ = "race_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(Integer)
    round = Column(Integer)
    race_name = Column(String)
    circuit = Column(String)
    date = Column(Date)
    driver_id = Column(String, ForeignKey("drivers.driver_id")) #References the drivers table, drivers_id column
    constructor_id = Column(String, ForeignKey("constructors.constructor_id")) #References the constructors table, constructors_id column
    position = Column(Integer, nullable=True) #Nullable = means column can allow NULL data input
    grid = Column(Integer)
    laps_completed = Column(Integer)
    status = Column(String)
    points = Column(Float)
    fastest_lap = Column(Boolean, default = False)

class QualifyingResult(Base):
    __tablename__ = "qualifying_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(Integer)
    round = Column(Integer)
    driver_id = Column(String, ForeignKey("drivers.driver_id")) # Q1/Q2/Q3 times stored as strings e.g. "1:28.412"
                                                                # nullable because not all drivers make it to Q2 or Q3
    q1_time = Column(String, nullable=True)
    q2_time = Column(String, nullable=True)
    q3_time = Column(String, nullable=True)
    position = Column(Integer)

class LapTime(Base):
    __tablename__ = "lap_times"

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(Integer)
    round = Column(Integer)
    driver_id = Column(String, ForeignKey("drivers.driver_id"))
    lap_number = Column(Integer)
    # Storing times in milliseconds as integers is cleaner than strings
    # e.g. 88412 instead of "1:28.412" — easier to sort and compare
    lap_time_ms = Column(Integer, nullable=True)
    sector_1_ms = Column(Integer, nullable=True)
    sector_2_ms = Column(Integer, nullable=True)
    sector_3_ms = Column(Integer, nullable=True)
    compound = Column(String, nullable=True)   # tyre compound e.g. "SOFT"
    is_personal_best = Column(Boolean, default=False)

class PitStop(Base):
    __tablename__ = "pit_stops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(Integer)
    round = Column(Integer)
    driver_id = Column(String, ForeignKey("drivers.driver_id"))
    stop_number = Column(Integer)
    lap = Column(Integer)
    duration_ms = Column(Integer, nullable=True)

class RaceWeather(Base):
    __tablename__ = "race_weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(Integer)
    round = Column(Integer)
    timestamp = Column(DateTime)
    air_temp_c = Column(Float, nullable=True)
    track_temp_c = Column(Float, nullable=True)
    humidity_pct = Column(Float, nullable=True)
    wind_speed_ms = Column(Float, nullable=True)
    rainfall = Column(Boolean, default=False)

class RefreshLog(Base):
    __tablename__ = "refresh_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    triggered_at = Column(DateTime, default=func.now())
    # "scheduled" = automatic hourly refresh, "manual" = user clicked button
    trigger_type = Column(String)
    status = Column(String)            # "success" or "error"
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)