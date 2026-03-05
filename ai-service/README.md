# AI Service (API-only)

This service is a self-contained FastAPI API.

## Endpoints
- `GET /health/live`
- `GET /health/ready`
- `POST /api/v1/generate`

## Run locally
```bash
pip install .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
