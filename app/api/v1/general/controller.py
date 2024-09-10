"""
This module contains the general controller for the service.
It handles all http requests that are not entity specific.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
async def health_check():
    return {"status": "healthy"}
