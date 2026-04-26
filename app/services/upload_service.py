from pathlib import Path
from datetime import datetime
import uuid

STORAGE_DIR = Path(__file__).parent.parent / "storage" / "uploads"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_file(file) -> dict:
    original_name = file.filename

    safe_name = f"title-kinolenta"

    file_path = STORAGE_DIR / safe_name

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {
        "filename": original_name,
        "file_path": str(file_path),
        "uploaded_at": datetime.utcnow(),
    }
