"""
This module contains the general controller for the service.
It handles all http requests that are not entity specific.
"""

from fastapi import APIRouter
from app.common.config import settings
from app.common.database import inspector

router = APIRouter()


@router.get("/health", status_code=200)
async def health_check():

    tables = inspector.get_table_names()

    password = settings.get("DATABASE_PASSWORD", None)
    masked_password = "*" * len(password) if password else "-----"
    resp = f"""
            DATABASE_NAME: {settings.get("DATABASE_NAME", "-----")}\n
            DATABASE_HOST: {settings.get("DATABASE_HOST", "-----")}\n
            DATABASE_PORT: {settings.get("DATABASE_PORT", "-----")}\n
            DATABASE_PASSWORD: {masked_password}\n
            DATABASE_USER: {settings.get("DATABASE_USER", "-----")}\n
            DATABASE_URL: {settings.get("DATABASE_URL", "-----")}\n
            PORT: {settings.get("PORT", "-----")}\n
            LOG_LEVEL: {settings.get("LOG_LEVEL", "-----")}\n
            ANALYTICS_FOLDER: {settings.get("ANALYTICS_FOLDER", "-----")}
            APP_VERSION: {settings.get("APP_VERSION", "-----")}
            DB TABLES (Ensure connection): {tables}
            """

    return {"settings": resp}
