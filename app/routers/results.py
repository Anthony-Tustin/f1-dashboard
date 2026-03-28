from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import RaceResult, QualifyingResult, Driver, Constructor
from dotenv import load_dotenv
import os

load_dotenv()

SEASON = int(os.getenv("F1_SEASON", 2025))

router = APIRouter(prefix="/results", tags=["Results"])

@router.get("/races")
async def get_race_results(db: AsyncSession = Depends(get_db)): #Returns all race results for the current season.
    
    result = await db.execute(
        select(RaceResult, Driver, Constructor)
        .join(Driver, RaceResult.driver_id == Driver.driver_id)
        .join(Constructor, RaceResult.constructor_id == Constructor.constructor_id)
        .where(RaceResult.season == SEASON)
        .order_by(RaceResult.round, RaceResult.position)
    )
    rows = result.all()

    return [
        {
            "round": r.round,
            "race_name": r.race_name,
            "circuit": r.circuit,
            "date": str(r.date),
            "position": r.position,
            "driver_name": d.full_name,
            "team_name": d.team_name,
            "grid": r.grid,
            "laps_completed": r.laps_completed,
            "status": r.status,
            "points": r.points,
            "fastest_lap": r.fastest_lap
        }
        for r, d, c in rows
    ]


@router.get("/races/{round_number}")
async def get_race_result_by_round(
    round_number: int,
    db: AsyncSession = Depends(get_db)
): #Returns results for a specific race round.  {round_number} in the URL is a path parameter

    result = await db.execute(
        select(RaceResult, Driver, Constructor)
        .join(Driver, RaceResult.driver_id == Driver.driver_id)
        .join(Constructor, RaceResult.constructor_id == Constructor.constructor_id)
        .where(RaceResult.season == SEASON)
        .where(RaceResult.round == round_number)
        .order_by(RaceResult.position)
    )
    rows = result.all()

    return [
        {
            "round": r.round,
            "race_name": r.race_name,
            "circuit": r.circuit,
            "date": str(r.date),
            "position": r.position,
            "driver_name": d.full_name,
            "team_name": d.team_name,
            "grid": r.grid,
            "laps_completed": r.laps_completed,
            "status": r.status,
            "points": r.points,
            "fastest_lap": r.fastest_lap
        }
        for r, d, c in rows
    ]


@router.get("/qualifying/{round_number}")
async def get_qualifying_results(
    round_number: int,
    db: AsyncSession = Depends(get_db)
): #Returns qualifying grid for a specific round.
    
    result = await db.execute(
        select(QualifyingResult, Driver)
        .join(Driver, QualifyingResult.driver_id == Driver.driver_id)
        .where(QualifyingResult.season == SEASON)
        .where(QualifyingResult.round == round_number)
        .order_by(QualifyingResult.position)
    )
    rows = result.all()

    return [
        {
            "position": q.position,
            "driver_name": d.full_name,
            "team_name": d.team_name,
            "q1_time": q.q1_time,
            "q2_time": q.q2_time,
            "q3_time": q.q3_time,
        }
        for q, d in rows
    ]