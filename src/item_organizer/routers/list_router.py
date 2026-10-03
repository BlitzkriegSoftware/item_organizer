from pathlib import Path

from fastapi import APIRouter

ListRouter = APIRouter(prefix="/v1/list", tags=["list"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
