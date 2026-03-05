from .health import router as health_router
from .generate import router as generate_router
from .results import router as results_router
from .stats import router as stats_router
from .components import router as components_router
from .test_routes import router as test_router
from .websocket import router as websocket_router

__all__ = [
    "health_router",
    "generate_router",
    "results_router",
    "stats_router",
    "components_router",
    "test_router",
    "websocket_router",
]
