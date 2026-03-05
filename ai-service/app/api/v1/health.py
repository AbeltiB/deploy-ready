from datetime import datetime, timezone
from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("/health/live", tags=["Health"])
async def live():
    return {
        "status": "alive",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/ready", tags=["Health"])
async def ready():
    return {
        "status": "ready",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
