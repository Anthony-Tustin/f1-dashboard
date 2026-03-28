#Sets up the APScheduler that automatically triggers a data refresh every hour 

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os

load_dotenv()

REFRESH_INTERVAL_HOURS = int(os.getenv("REFRESH_INTERVAL_HOURS", 1)) #initialises the hourly refresh of the data

scheduler = AsyncIOScheduler() #Creates the scheduler instance

def start_scheduler():
    from app.ingestion.ingest import ingest #Circular import - loading within a function, waits until everything is already loaded before imports.
    scheduler.add_job(
        ingest,                          # the function to call
        trigger="interval",              # run on a repeating interval
        hours=REFRESH_INTERVAL_HOURS,    # every 1 hour
        id="hourly_ingest",              # unique name for this job
        replace_existing=True,           # replace if already registered
        misfire_grace_time=300           # 5 min grace period if server is busy, ensures data is still collected even when server is busy with requests
    )

    scheduler.start()

def stop_scheduler():
    if scheduler.running:
            scheduler.shutdown()