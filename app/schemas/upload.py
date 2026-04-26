from pydantic import BaseModel
from datetime import datetime


class UploadResponse(BaseModel):
    filename: str
    file_path: str
    uploaded_at: datetime