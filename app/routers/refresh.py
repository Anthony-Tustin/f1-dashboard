from fastapi import APIRouter
from app.ingestion.ingest import ingest
import time

router = APIRouter(prefix="/refresh", tags=["Refresh"])

@router.post("")
async def manual_refresh(): #Triggers an immediate data refresh. Called by the refresh button in the frontend UI.
    
    print("Manual refresh triggered...")
    start = time.time()

    try:
        await ingest()
        duration_ms = int((time.time() - start) * 1000)
        return {
            "status": "success",
            "message": "Data refreshed successfully",
            "duration_ms": duration_ms
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/status")
async def refresh_status(): #Returns the last time data was refreshed. Frontend uses this to show latest update.
    
    from app.database import AsyncSessionLocal
    from app.models import RefreshLog
    from sqlalchemy import select

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RefreshLog)
            .order_by(RefreshLog.triggered_at.desc())
            .limit(1)
        )
        last = result.scalar_one_or_none()

    if last is None:
        return {"last_refresh": None, "status": "never"}

    return {
        "last_refresh": last.triggered_at,
        "status": last.status,
        "trigger_type": last.trigger_type,
        "duration_ms": last.duration_ms
    }