from typing import Dict
from fastapi import APIRouter


router = APIRouter()


@router.get("/health", tags=["API Helath"])
async def health() -> Dict[str, str]:
    return {"health": "All is good!"}