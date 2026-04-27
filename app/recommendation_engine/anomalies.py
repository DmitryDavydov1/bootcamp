import pandas as pd

from app.recommendation_engine.config import (
    CTR_FEED_ANOMALY_THRESHOLD,
    MIN_VIEWS_SMALL_SAMPLE,
    CLASSIC_KEYWORDS,
    BOSS_KEYWORDS,
)


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
