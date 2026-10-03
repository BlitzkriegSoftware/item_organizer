from pathlib import Path

from fastapi import APIRouter

ReportingRouter = APIRouter(prefix="/v1/reporting", tags=["reporting"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
