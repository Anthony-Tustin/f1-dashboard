from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models import DriverStanding, ConstructorStanding, Driver, Constructor
from dotenv import load_dotenv
import os

load_dotenv()

SEASON = int(os.getenv("F1_SEASON", 2025))

router = APIRouter(prefix="/standings", tags=["standings"])
#We give APIROUTER a pre fix so every route here starts with /standings


#Returns current driver championship, ordered by position
@router.get("/drivers")
async def get_driver_standings(db: AsyncSession = Depends(get_db)): #FastAPI automatically opens a database session and passes it in
    result = await db.execute(
        select(DriverStanding, Driver)
        .join(Driver, DriverStanding.driver_id == Driver.driver_id)
        .where(DriverStanding.season == SEASON)
        .order_by(DriverStanding.position)
    )
    rows = result.all()

    return [
        {
            "position": standing.position,
            "driver_id": standing.driver_id,
            "full_name": driver.full_name,
            "team_name": driver.team_name,
            "points": standing.points,
            "wins": standing.wins
        }
        for standing, driver in rows
    ]

@router.get("/constructors")
async def get_constructor_standings(db: AsyncSession = Depends(get_db)):
    """
    Returns current constructor championship standings ordered by position.
    """
    result = await db.execute(
        select(ConstructorStanding, Constructor)
        .join(Constructor, ConstructorStanding.constructor_id == Constructor.constructor_id)
        .where(ConstructorStanding.season == SEASON)
        .order_by(ConstructorStanding.position)
    )
    rows = result.all()

    return [
        {
            "position": standing.position,
            "constructor_id": standing.constructor_id,
            "name": constructor.name,
            "points": standing.points,
            "wins": standing.wins
        }
        for standing, constructor in rows
    ]