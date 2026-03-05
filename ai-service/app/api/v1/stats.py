from datetime import datetime, timezone
from fastapi import APIRouter

from app.services.runtime_store import runtime_store
from app.services.pipeline import pipeline

router = APIRouter()


@router.get("/stats", tags=["Statistics"])
async def get_stats():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_steps": pipeline.stage_order,
        "runtime": runtime_store.stats(),
    }
