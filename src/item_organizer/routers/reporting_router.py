from pathlib import Path

from fastapi import APIRouter

from item_organizer.middleware.logging_route import LoggingRoute

ReportingRouter = APIRouter(
    prefix="/v1/reporting", tags=["reporting"], route_class=LoggingRoute
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
