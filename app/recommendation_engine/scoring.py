import pandas as pd

from app.recommendation_engine.config import (
    MIN_CAROUSEL_IMPRESSIONS,
    CAROUSEL_WEIGHTS,
    TOP10_WEIGHTS,
    HOT_WEIGHTS,
)


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
