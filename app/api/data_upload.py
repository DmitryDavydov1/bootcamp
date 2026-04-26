from fastapi import APIRouter, UploadFile, File

from app.services.upload_service import save_file
from app.schemas.upload import UploadResponse

router = APIRouter(prefix="/api/data", tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    result = save_file(file)
    return result