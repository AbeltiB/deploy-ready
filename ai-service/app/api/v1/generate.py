from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.pipeline import run_pipeline
from app.services.runtime_store import runtime_store

router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=2000)


@router.post("/generate", tags=["Generation"])
async def generate_app(request: GenerateRequest):
    output = run_pipeline(request.prompt)
    runtime_store.add_result(output)
    return output
