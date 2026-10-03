from pathlib import Path

from fastapi import APIRouter

UserRouter = APIRouter(prefix="/v1/users", tags=["users"])
PROJECT_ROOT = Path(__file__).resolve().parents[3]
