from fastapi import APIRouter

router = APIRouter()


@router.get("/test/ping", tags=["Test"])
async def ping():
    return {"status": "ok"}
