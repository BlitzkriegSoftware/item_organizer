import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

HomeRouter = APIRouter(prefix="/", tags=["home"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@HomeRouter.get("", tags=["home"])
async def home_page():
    index_page = PROJECT_ROOT / "www" / "page" / "index.html"
    if not os.path.exists(index_page):
        raise HTTPException(status_code=404, detail="File not found")

    with open(index_page, "r", encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content)
