from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import LapTime, PitStop, RaceWeather, Driver
from dotenv import load_dotenv
import os

load_dotenv()

SEASON = int(os.getenv("F1_SEASON", 2025))

router = APIRouter(prefix="/laps", tags=["Laps"])

@router.get("/{round_number}/{driver_id}")
async def get_lap_times(
    round_number: int, 
    driver_id: str, 
    db: AsyncSession = Depends(get_db)
): #Returns all lap times for a specific driver for a specfic race
    
    result = await db.execute(
        select(LapTime)
        .where(LapTime.season == SEASON)
        .where(LapTime.round == round_number)
        .where(LapTime.driver_id == driver_id)
        .order_by(LapTime.lap_number)
    )
    laps = result.scalars().all()

    return [
        {
            "lap_number": lap.lap_number,
            "lap_time_ms": lap.lap_time_ms,
            "sector_1_ms": lap.sector_1_ms,
            "sector_2_ms": lap.sector_2_ms,
            "sector_3_ms": lap.sector_3_ms,
            "compound": lap.compound,
            "is_personal_best": lap.is_personal_best

        }
        for lap in laps
    ]

@router.get("/pitstops/{round_number}")
async def get_pit_stops(
    round_number: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Returns all pit stops for a specific race round.
    """
    result = await db.execute(
        select(PitStop, Driver)
        .join(Driver, PitStop.driver_id == Driver.driver_id)
        .where(PitStop.season == SEASON)
        .where(PitStop.round == round_number)
        .order_by(PitStop.lap)
    )
    rows = result.all()

    return [
        {
            "driver_name": driver.full_name,
            "stop_number": pit.stop_number,
            "lap": pit.lap,
            "duration_ms": pit.duration_ms
        }
        for pit, driver in rows
    ]


@router.get("/weather/{round_number}")
async def get_weather(
    round_number: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Returns weather data for a specific race weekend.
    """
    result = await db.execute(
        select(RaceWeather)
        .where(RaceWeather.season == SEASON)
        .where(RaceWeather.round == round_number)
        .order_by(RaceWeather.timestamp)
    )
    weather = result.scalars().all() #unwrap the result into a simple list of objects rather than pairs.

    return [
        {
            "timestamp": str(w.timestamp),
            "air_temp_c": w.air_temp_c,
            "track_temp_c": w.track_temp_c,
            "humidity_pct": w.humidity_pct,
            "wind_speed_ms": w.wind_speed_ms,
            "rainfall": w.rainfall
        }
        for w in weather
    ]