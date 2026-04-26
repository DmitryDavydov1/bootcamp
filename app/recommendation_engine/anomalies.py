import re
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional

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


def flag_classic(title: str) -> bool:
    return any(kw in title.lower() for kw in CLASSIC_KEYWORDS)


def flag_boss(title: str) -> bool:
    return any(kw in title.lower() for kw in BOSS_KEYWORDS)


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["anomaly_ctr_feed"] = df["ctr_feed"] > CTR_FEED_ANOMALY_THRESHOLD
    df["flag_classic"] = df["title"].apply(flag_classic)
    df["flag_small_views"] = df["views"] < MIN_VIEWS_SMALL_SAMPLE
    return df
