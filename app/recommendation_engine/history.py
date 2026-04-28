import json
from pathlib import Path


HISTORY_FILE = Path(__file__).parent / "output" / "history.json"


def load_history() -> dict:
    if not HISTORY_FILE.exists():
        return {}

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(
    history: dict,
    app: str,
    lang: str,
    today: str,
    carousel_titles: list,
    top10_titles: list,
    hot_titles: list,
    rating_titles: list,
    rating_values: list,
) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    key = f"{app}-{lang}"
    runs = history.get(key, [])

    new_run = {
        "date": today,
        "carousel": carousel_titles,
        "top10": top10_titles,
        "hot": hot_titles,
        "ratings": dict(zip(rating_titles, rating_values)),
    }

    # Чтобы повторное нажатие "Сгенерировать отчет" в тот же день
    # не накручивало историю ротации.
    runs = [run for run in runs if run.get("date") != today]
    runs.append(new_run)

    history[key] = runs[-12:]

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)