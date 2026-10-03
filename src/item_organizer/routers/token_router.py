from pathlib import Path

from fastapi import APIRouter

TokenRouter = APIRouter(prefix="/v1/token", tags=["token"])
PROJECT_ROOT = Path(__file__).resolve().parents[3]
