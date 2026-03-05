from fastapi import APIRouter

from app.models.schemas.component_catalog import COMPONENT_DEFINITIONS, get_available_components

router = APIRouter()


@router.get("/components", tags=["Components"])
async def get_components():
    return {
        "available_components": get_available_components(),
        "catalog": COMPONENT_DEFINITIONS,
    }
