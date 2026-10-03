from pathlib import Path

from fastapi import APIRouter

PageRouter = APIRouter(prefix="/v1/page", tags=["page"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
