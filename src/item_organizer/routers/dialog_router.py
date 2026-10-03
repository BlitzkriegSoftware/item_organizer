from fastapi import APIRouter

from item_organizer.middleware.logging_route import LoggingRoute

DialogRouter = APIRouter(prefix="/v1/dialog", tags=["dialog"], route_class=LoggingRoute)
