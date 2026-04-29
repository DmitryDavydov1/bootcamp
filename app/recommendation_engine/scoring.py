import numpy as np
import pandas as pd

from app.recommendation_engine.config import (
    CAROUSEL_WEIGHTS,
    TOP10_WEIGHTS,
    HOT_WEIGHTS,
)


def calc_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- CTR с учетом confidence ---
    df["ctr_carousel_eff"] = ctr_confidence(
        df["ctr_carousel"], df["carousel_impressions"]
    )

    df["ctr_feed_eff"] = ctr_confidence(
        df["ctr_feed"], df["feed_impressions"]
    )

    df.loc[df["anomaly_ctr_feed"], "ctr_feed_eff"] = 0

    # --- RETENTION SCORE ---
    df["retention_score"] = (
            0.4 * df.get("retention_3", 0) +
            0.3 * df.get("retention_5", 0) +
            0.2 * df.get("retention_10", 0) +
            0.1 * df.get("retention_30", 0)
    )

    # --- ENGAGEMENT ---
    df["engagement"] = (
            0.4 * df["bwr"] +
            0.3 * df["depth"] +
            0.3 * df["retention_score"]
    )

    # --- TREND (прокси) ---
    df["trend"] = df["ctr_feed"] * df["feed_impressions"]

    # --- Нормализация ---
    n = {
        "views": minmax_norm(df["views"], log_scale=True),
        "total_time": minmax_norm(df["total_time"], log_scale=True),
        "bwr": minmax_norm(df["bwr"]),
        "depth": minmax_norm(df["depth"]),
        "engagement": minmax_norm(df["engagement"]),
        "retention": minmax_norm(df["retention_score"]),
        "trend": minmax_norm(df["trend"]),
        "ctr_carousel": minmax_norm(df["ctr_carousel_eff"]),
        "ctr_feed": minmax_norm(df["ctr_feed_eff"]),
        "source_feed": minmax_norm(df["source_feed"]),
    }

    # --- CAROUSEL ---
    w = CAROUSEL_WEIGHTS
    df["carousel_score"] = (
            n["ctr_carousel"] * w["ctr_carousel"] +
            n["engagement"] * w["engagement"] +
            n["retention"] * w["retention"] +
            n["views"] * w["views"]
    )

    # --- TOP10 ---
    w = TOP10_WEIGHTS
    df["top10_score"] = (
            n["views"] * w["views"] +
            n["total_time"] * w["total_time"] +
            n["retention"] * w["retention"] +
            n["engagement"] * w["engagement"]
    )

    # --- HOT ---
    w = HOT_WEIGHTS
    df["hot_score"] = (
            n["ctr_feed"] * w["ctr_feed"] +
            n["source_feed"] * w["source_feed"] +
            n["engagement"] * w["engagement"] +
            n["views"] * w["views"]
    )

    return df


def ctr_confidence(ctr: pd.Series, impressions: pd.Series, scale: float = 50):
    return ctr * (1 - np.exp(-impressions / scale))


def minmax_norm(
        series: pd.Series,
        log_scale: bool = False,
        lower_q: float = 0.01,
        upper_q: float = 0.99
) -> pd.Series:
    s = series.copy().astype(float)

    if log_scale:
        s = np.log1p(s.clip(lower=0))

    q_low, q_high = s.quantile([lower_q, upper_q])
    s = s.clip(q_low, q_high)

    if q_high == q_low:
        return pd.Series(0.0, index=s.index)

    return (s - q_low) / (q_high - q_low)
