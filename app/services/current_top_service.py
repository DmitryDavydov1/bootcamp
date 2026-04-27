import json
from pathlib import Path
from datetime import datetime
from typing import Any

CURRENT_TOP_PATH = (
    Path(__file__).parent.parent
    / "recommendation_engine"
    / "output"
    / "current_top.json"
)

DEFAULT_CURRENT_TOP = {
    "carousel": [],
    "top10": [],
    "hot": [],
    "saved_at": None,
}


def get_current_top() -> dict[str, Any]:
    if not CURRENT_TOP_PATH.exists():
        return DEFAULT_CURRENT_TOP

    with open(CURRENT_TOP_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_current_top(data: dict[str, Any]) -> dict[str, Any]:
    CURRENT_TOP_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "carousel": data.get("carousel", []),
        "top10": data.get("top10", []),
        "hot": data.get("hot", []),
        "saved_at": datetime.utcnow().isoformat(),
    }

    with open(CURRENT_TOP_PATH, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return payload