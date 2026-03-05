# Deploy-ready API-only stack

This repository now contains only a deployable API service and its docker infrastructure.

## Start with Docker Compose
```bash
cd infra
docker compose up --build
```

## API
- `GET /health/live`
- `GET /health/ready`
- `POST /api/v1/generate`
