from pathlib import Path

from fastapi import APIRouter

OrgRouter = APIRouter(prefix="/v1/org", tags=["org"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
