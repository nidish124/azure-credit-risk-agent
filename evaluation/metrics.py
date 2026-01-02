from fastapi import APIRouter
from evaluation.registry import MetricsRegistry

router = APIRouter(
    prefix="/metrics",
    tags=["metrics"]
)

@router.get("", summary="System evaluation metrics")
def get_metrics():
    """
    Read-only endpoint exposing system evaluation metrics.
    Intended for observability and monitoring only.
    """
    return {
        "status": "ok",
        "metrics": MetricsRegistry.snapshot()
    }
