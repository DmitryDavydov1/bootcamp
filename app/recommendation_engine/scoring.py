import pandas as pd
from pathlib import Path

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




def calc_scores(df: pd.DataFrame,
                carousel_imp_threshold: int = MIN_CAROUSEL_IMPRESSIONS) -> pd.DataFrame:
    df = df.copy()
    ctr_car_eff = df["ctr_carousel"].copy()
    ctr_car_eff[df["carousel_impressions"] < carousel_imp_threshold] = 0
    ctr_feed_eff = df["ctr_feed"].copy()
    ctr_feed_eff[df["anomaly_ctr_feed"]] = 0

    df["ctr_carousel_eff"] = ctr_car_eff
    df["ctr_feed_eff"] = ctr_feed_eff

    n = {
        "views": minmax_norm(df["views"]),
        "total_time": minmax_norm(df["total_time"]),
        "bwr": minmax_norm(df["bwr"]),
        "depth": minmax_norm(df["depth"]),
        "source_feed": minmax_norm(df["source_feed"]),
        "ctr_carousel": minmax_norm(df["ctr_carousel_eff"]),
        "ctr_feed": minmax_norm(df["ctr_feed_eff"]),
    }

    w = CAROUSEL_WEIGHTS
    df["carousel_score"] = (
            n["ctr_carousel"] * w["ctr_carousel"] +
            n["views"] * w["views"] +
            n["depth"] * w["depth"] +
            n["bwr"] * w["bwr"]
    )
    w = TOP10_WEIGHTS
    df["top10_score"] = (
            n["views"] * w["views"] +
            n["total_time"] * w["total_time"] +
            n["depth"] * w["depth"] +
            n["bwr"] * w["bwr"]
    )
    w = HOT_WEIGHTS
    df["hot_score"] = (
            n["ctr_feed"] * w["ctr_feed"] +
            n["source_feed"] * w["source_feed"] +
            n["bwr"] * w["bwr"] +
            n["views"] * w["views"]
    )
    return df


def minmax_norm(series: pd.Series) -> pd.Series:
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - mn) / (mx - mn)
