from pathlib import Path
from datetime import datetime
import shutil

from fastapi import UploadFile


STORAGE_DIR = Path(__file__).parent.parent / "storage" / "uploads"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_file_as(file: UploadFile, target_filename: str) -> dict:
    original_name = file.filename

    if not original_name:
        raise ValueError("Файл не выбран")

    if not original_name.lower().endswith(".csv"):
        raise ValueError("Можно загружать только CSV-файлы")

    file_path = STORAGE_DIR / target_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": original_name,
        "file_path": str(file_path),
        "uploaded_at": datetime.utcnow(),
    }