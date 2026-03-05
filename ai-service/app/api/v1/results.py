from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict

from app.services.runtime_store import runtime_store
from app.utils.output_JSON_formatter import format_pipeline_output, validate_output

router = APIRouter()


class ConvertRequest(BaseModel):
    payload: Dict[str, Any] = Field(..., description="Raw pipeline payload")


@router.get("/results/latest", tags=["Results"])
async def latest_result():
    latest = runtime_store.latest()
    if not latest:
        raise HTTPException(status_code=404, detail="No results generated yet")
    return latest


@router.get("/results", tags=["Results"])
async def list_results(limit: int = 10):
    return {"items": runtime_store.list_results(limit=limit)}


@router.post("/results/convert", tags=["Results"])
async def convert_result(request: ConvertRequest):
    converted = format_pipeline_output(request.payload)
    valid, errors = validate_output(converted)
    return {
        "valid": valid,
        "errors": errors,
        "result": converted,
    }
