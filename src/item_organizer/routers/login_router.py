from pathlib import Path

from fastapi import APIRouter

LoginRouter = APIRouter(prefix="/v1/login", tags=["login"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
