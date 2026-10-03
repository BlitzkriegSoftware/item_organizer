from pathlib import Path

from fastapi import APIRouter

ItemRouter = APIRouter(prefix="/v1/item", tags=["item"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
