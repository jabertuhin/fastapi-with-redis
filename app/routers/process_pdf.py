from typing import Dict

from fastapi import APIRouter, UploadFile, File
from fastapi.param_functions import Depends


router = APIRouter(prefix="/pdf")


@router.post("/extract", tags=["PDF Info Extraction"])
async def extract(file: UploadFile = File(...)):
    return {"message": "Successfully Uploaded!"}