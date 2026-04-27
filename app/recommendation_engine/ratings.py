import pandas as pd

from app.recommendation_engine.scoring import minmax_norm
from app.recommendation_engine.config import (
    RATING_WEIGHTS,
    ROTATION_PENALTY,
    FRESHNESS_BOOST,
)


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
