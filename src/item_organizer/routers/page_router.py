from pathlib import Path

from fastapi import APIRouter

from item_organizer.middleware.logging_route import LoggingRoute

PageRouter = APIRouter(prefix="/v1/page", tags=["page"], route_class=LoggingRoute)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
