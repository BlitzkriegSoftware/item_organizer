from varname import nameof

from app_logger.applogger import AppLogger
import json
import os
from pathlib import Path
from typing import List
from pydantic import BaseModel, field_validator
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from functools import cache
import uvicorn


"""
Must set a CORS policy, this one is not suitable for production!
expose_headers must include the list of 'hx-' headers you plan to use!
"""
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["hx-trigger"],
)


def main():
    port = int(os.getenv("IOR_APP_PORT", 8097))
    message: str = f"item-organizer start up on port: {port}"
    AppLogger.log_info(message, {}, logger_name=nameof(main))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
