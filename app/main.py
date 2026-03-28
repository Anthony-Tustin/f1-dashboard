from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.scheduler import start_scheduler, stop_scheduler
from app import models # Import all models so SQLAlchemy knows about them when creating table
from app.routers import standings, refresh, results, laps

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting F1 Dashboard...")
    async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all) #reads all the classes in models.py that inherit their data from Base, creates tables if they don't already exist
                                                            #create_all = creates the table structures, but doesn't populate them 
    print("Database tables ready.") #displays when tables are ready
    
    start_scheduler() #runs the hourly scheduler function 
    print("Scheduler started.")

    yield #The app runs here, everything after yeild runs on SHUTDOWN of Application

    stop_scheduler()
    print("Scheduler stopped. Goodbye")


#Creating the FastAPI application and attaching the Lifespan variables
app = FastAPI(
    title="F1 Dashboard API",
    description="Live Formula One data powered by FastF1",
    version="1.0.0",
    lifespan=lifespan
)

#Front end accessible at http://localhost:8000
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(standings.router)
app.include_router(refresh.router)
app.include_router(results.router)
app.include_router(laps.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "F1 Dashboard is running"}

