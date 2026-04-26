import pandas as pd
from pathlib import Path

from app.recommendation_engine.scoring import minmax_norm

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"

# Минимальные пороги (стандартные)
MIN_CAROUSEL_IMPRESSIONS = 100
MIN_FEED_IMPRESSIONS = 20
MIN_VIEWS_TOP10 = 50
MIN_VIEWS_SMALL_SAMPLE = 30
CTR_FEED_ANOMALY_THRESHOLD = 50

# Пониженные пороги (применяются если стандартных кандидатов не хватает)
MIN_CAROUSEL_IMPRESSIONS_LOW = 30
MIN_FEED_IMPRESSIONS_LOW = 5
MIN_VIEWS_TOP10_LOW = 20

# Минимально допустимое число кандидатов прежде чем снижать пороги
MIN_CANDIDATES_CAROUSEL = 8
MIN_CANDIDATES_TOP10 = 8
MIN_CANDIDATES_HOT = 8

# Веса формул
CAROUSEL_WEIGHTS = {"ctr_carousel": 0.35, "views": 0.25, "depth": 0.20, "bwr": 0.20}
TOP10_WEIGHTS = {"views": 0.40, "total_time": 0.30, "depth": 0.20, "bwr": 0.10}
HOT_WEIGHTS = {"ctr_feed": 0.35, "source_feed": 0.25, "bwr": 0.25, "views": 0.15}

# Количество кандидатов в каждую подборку
N_CAROUSEL = 15
N_TOP10 = 15
N_HOT = 20
N_RATING = 20

# Веса BASE_SCORE для рейтингов
RATING_WEIGHTS = {
    "ctr_feed": 0.30,
    "ctr_carousel": 0.20,
    "views": 0.20,
    "bwr": 0.15,
    "depth": 0.10,
    "source_feed": 0.05,
}

# Штраф за долгую ротацию
ROTATION_PENALTY = {4: 0.85, 6: 0.70}
FRESHNESS_BOOST = 1.15

BOSS_KEYWORDS = ["босс", "директор", "миллиардер", "начальник", "ceo", "шеф"]
CLASSIC_KEYWORDS = [
    "броненосец", "волга", "весёлые ребята", "садко", "цирк", "свинарка",
    "подкидыш", "тимур", "белый клык", "небесный тихоход", "шофер",
    "каменный цветок", "дети капитана"
]





def calc_ratings(df: pd.DataFrame, app: str, lang: str, history: dict) -> pd.DataFrame:
    df = df.copy()
    ctr_feed_eff = df["ctr_feed"].copy()
    ctr_feed_eff[df["anomaly_ctr_feed"]] = 0

    n = {
        "ctr_feed": minmax_norm(ctr_feed_eff),
        "ctr_carousel": minmax_norm(df["ctr_carousel"]),
        "views": minmax_norm(df["views"]),
        "bwr": minmax_norm(df["bwr"]),
        "depth": minmax_norm(df["depth"]),
        "source_feed": minmax_norm(df["source_feed"]),
    }
    w = RATING_WEIGHTS
    df["base_score"] = (
            n["ctr_feed"] * w["ctr_feed"] +
            n["ctr_carousel"] * w["ctr_carousel"] +
            n["views"] * w["views"] +
            n["bwr"] * w["bwr"] +
            n["depth"] * w["depth"] +
            n["source_feed"] * w["source_feed"]
    )

    key = f"{app}-{lang}"
    runs = history.get(key, [])

    def runs_in_tops(title: str) -> int:
        count = 0
        for run in reversed(runs):
            if title in run.get("carousel", []) or title in run.get("hot", []):
                count += 1
            else:
                break
        return count

    def ever_in_tops(title: str) -> bool:
        return any(
            title in run.get("carousel", []) or
            title in run.get("hot", []) or
            title in run.get("top10", [])
            for run in runs
        )

    def rotation_penalty(title: str) -> float:
        n_r = runs_in_tops(title)
        if n_r >= 6: return ROTATION_PENALTY[6]
        if n_r >= 4: return ROTATION_PENALTY[4]
        return 1.0

    def freshness_boost(title: str) -> float:
        return 1.0 if ever_in_tops(title) else FRESHNESS_BOOST

    df["rotation_penalty"] = df["title"].apply(rotation_penalty)
    df["freshness_boost"] = df["title"].apply(freshness_boost)
    df["rating_score"] = df["base_score"] * df["rotation_penalty"] * df["freshness_boost"]
    df["rating"] = (df["rating_score"] * 100).round().astype(int).clip(1, 100)
    return df
