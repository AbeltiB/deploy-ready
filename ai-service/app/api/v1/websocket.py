from fastapi import APIRouter

router = APIRouter()


@router.get("/ws/info", tags=["WebSocket"])
async def websocket_info():
    return {
        "enabled": False,
        "message": "WebSocket streaming is disabled in API-only mode; use synchronous /api/v1/generate.",
    }
