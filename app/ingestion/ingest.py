from app.database import AsyncSessionLocal
from app.ingestion.standings import fetch_driver_standings, fetch_constructor_standings
from dotenv import load_dotenv
import os

load_dotenv()

SEASON = int(os.getenv("F1_SEASON", 2025))


async def ingest():# Master ingestion function, called by the scheduler every hour and by the manual refresh button of the user.
    print(f"Starting full data refresh for {SEASON} season...")

    async with AsyncSessionLocal() as session:
        await fetch_driver_standings(session, SEASON)
        await fetch_constructor_standings(session, SEASON)

    print("Data refresh complete.")