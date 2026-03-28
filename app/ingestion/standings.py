import fastf1
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models import Driver, Constructor, DriverStanding, ConstructorStanding
from dotenv import load_dotenv
import os

load_dotenv()

# Tell FastF1 where to cache data locally, this means repeat fetches are instant instead of using the API every time
CACHE_DIR = os.getenv("CACHE_DIR", "./cache")
fastf1.Cache.enable_cache(CACHE_DIR)

async def fetch_driver_standings(session: AsyncSession, season: int): # Fetches current driver championship standings via FastF1 and upserts them into the database.
    print(f"Fetching driver standings for {season}...")

    # Uses the Ergast API under the hood for standings data
    from fastf1.ergast import Ergast
    ergast = Ergast()
    result = ergast.get_driver_standings(season=season, round="last")
    standings = result.content[0]

    if standings is None or standings.empty:
        print("No driver standings data available.")
        return
    
    for _, row in standings.iterrows():
        driver_stmt = insert(Driver).values(
            driver_id=row["driverId"],
            code=row.get("code", None),
            full_name=f"{row['givenName']} {row['familyName']}",
            team_name=row.get("constructorNames", [None])[0],
            nationality=row.get("nationality", None),
            permanent_number=row.get("permanentNumber", None)
        ).on_conflict_do_update(
            index_elements=["driver_id"],
            set_=dict(
                full_name=f"{row['givenName']} {row['familyName']}",
                team_name=row.get("constructorNames", [None])[0],
            )
        )
        await session.execute(driver_stmt)

        #Upsert the standing itself
        standing_stmt = insert(DriverStanding).values(
            driver_id=row["driverId"],
            season=season,
            position=int(row["position"]),
            points=float(row["points"]),
            wins=int(row["wins"])
        ).on_conflict_do_update(
            index_elements=["driver_id", "season"],
            set_=dict(
                position=int(row["position"]),
                points=float(row["points"]),
                wins=int(row["wins"])
            )
        )
        await session.execute(standing_stmt)

        await session.commit()
        print(f"Driver standings saved - {len(standings)} drivers.")

async def fetch_constructor_standings(session: AsyncSession, season: int):# Fetches current constructor championship standings via FastF1 and upserts them into the database.

    print(f"Fetching constructor standings for {season}...")

    from fastf1.ergast import Ergast
    ergast = Ergast()
    result = ergast.get_constructor_standings(season=season, round="last")
    standings = result.content[0]

    if standings is None or standings.empty:
        print("No constructor standings data available.")
        return

    for _, row in standings.iterrows():  # First upsert the constructor into the constructors table
        constructor_stmt = insert(Constructor).values(
            constructor_id=row["constructorId"],
            name=row["constructorName"],
            nationality=row.get("nationality", None)
        ).on_conflict_do_update(
            index_elements=["constructor_id"],
            set_=dict(name=row["constructorName"])
        )
        await session.execute(constructor_stmt)

        # Now upsert the standing
        standing_stmt = insert(ConstructorStanding).values(
            constructor_id=row["constructorId"],
            season=season,
            position=int(row["position"]),
            points=float(row["points"]),
            wins=int(row["wins"])
        ).on_conflict_do_update(
            index_elements=["constructor_id", "season"],
            set_=dict(
                position=int(row["position"]),
                points=float(row["points"]),
                wins=int(row["wins"])
            )
        )
        await session.execute(standing_stmt)

    await session.commit()
    print(f"Constructor standings saved — {len(standings)} constructors.")