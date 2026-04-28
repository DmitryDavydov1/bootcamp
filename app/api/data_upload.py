from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.upload_service import save_file_as
from app.schemas.upload import UploadResponse


router = APIRouter(prefix="/api/data", tags=["upload"])


@router.post("/upload-title", response_model=UploadResponse)
async def upload_title_file(file: UploadFile = File(...)):
    try:
        return save_file_as(file, "title-kinolenta.csv")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/upload-ctr", response_model=UploadResponse)
async def upload_ctr_file(file: UploadFile = File(...)):
    try:
        return save_file_as(file, "ctr-kinolenta.csv")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))