from datetime import datetime

import pandas as pd

from app.services.dataset_service import load_dataset
from app.recommendation_engine.anomalies import detect_anomalies
from app.recommendation_engine.shelves import build_unique_shelves
from app.recommendation_engine.ratings import calc_ratings
from app.recommendation_engine.history import load_history, save_history
from app.recommendation_engine.config import (
    CTR_FEED_ANOMALY_THRESHOLD,
    MIN_CAROUSEL_IMPRESSIONS,
    MIN_FEED_IMPRESSIONS,
    MIN_VIEWS_TOP10,
    N_RATING,
)


APP_NAME = "kinolenta"
LANG = "ru"

NUMERIC_COLUMNS = [
    "views",
    "total_time",
    "bwr",
    "depth",
    "source_feed",
    "ctr_carousel",
    "ctr_feed",
    "carousel_impressions",
    "feed_impressions",
]


def generate_recommendations():
    titles_df, ctr_df = load_dataset()

    df = _prepare_dataframe(titles_df, ctr_df)
    df = detect_anomalies(df)

    history = load_history()
    shelves = build_unique_shelves(df)

    carousel_df = shelves["carousel"]
    top10_df = shelves["top10"]
    hot_df = shelves["hot"]
    df_scored = shelves["df_scored"]

    recommended_ratings_df = _build_recommended_ratings(
        df_scored=df_scored,
        history=history,
    )

    excluded_titles = _build_excluded_titles(df)

    carousel = _records_from_df(
        carousel_df,
        fields=[
            "ctr_carousel",
            "carousel_impressions",
            "views",
            "depth",
            "bwr",
            "carousel_score",
        ],
        shelf="carousel",
        lowered=shelves["lowered_carousel"],
    )

    top10 = _records_from_df(
        top10_df,
        fields=[
            "views",
            "total_time",
            "depth",
            "bwr",
            "top10_score",
        ],
        shelf="top10",
        lowered=shelves["lowered_top10"],
    )

    hot = _records_from_df(
        hot_df,
        fields=[
            "ctr_feed",
            "feed_impressions",
            "source_feed",
            "bwr",
            "views",
            "hot_score",
        ],
        shelf="hot",
        lowered=shelves["lowered_hot"],
    )

    recommended_ratings = _rating_records_from_df(recommended_ratings_df)

    today = datetime.utcnow().date().isoformat()

    save_history(
        history=history,
        app=APP_NAME,
        lang=LANG,
        today=today,
        carousel_titles=list(carousel_df["title"]),
        top10_titles=list(top10_df["title"]),
        hot_titles=list(hot_df["title"]),
        rating_titles=list(recommended_ratings_df["title"]),
        rating_values=list(recommended_ratings_df["rating"].astype(int)),
    )

    return {
        "meta": {
            "app": APP_NAME,
            "lang": LANG,
            "generated_at": datetime.utcnow().isoformat(),
            "warnings": _build_warnings(shelves),
            "counts": {
                "carousel": len(carousel),
                "top10": len(top10),
                "hot": len(hot),
                "recommended_ratings": len(recommended_ratings),
                "excluded_titles": len(excluded_titles),
            },
        },
        "carousel": carousel,
        "top10": top10,
        "hot": hot,
        "recommended_ratings": recommended_ratings,
        "excluded_titles": excluded_titles,
    }


def _prepare_dataframe(titles_df: pd.DataFrame, ctr_df: pd.DataFrame | None) -> pd.DataFrame:
    df = titles_df.copy()

    if ctr_df is not None:
        df = df.merge(ctr_df, on="title", how="left")

    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            df[column] = 0

        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["title"] = df["title"].fillna("").astype(str).str.strip()
    df = df[df["title"] != ""]

    return df.fillna(0)


def _build_recommended_ratings(df_scored: pd.DataFrame, history: dict) -> pd.DataFrame:
    df_rated = calc_ratings(df_scored, APP_NAME, LANG, history)

    rating_df = (
        df_rated[~df_rated["anomaly_ctr_feed"]]
        .sort_values("rating_score", ascending=False)
        .head(N_RATING)
        .reset_index(drop=True)
    )

    rating_df.index += 1

    return rating_df


def _build_excluded_titles(df: pd.DataFrame) -> list[dict]:
    anomalies = (
        df[df["anomaly_ctr_feed"]]
        .sort_values("ctr_feed", ascending=False)
        .reset_index(drop=True)
    )

    return [
        {
            "title": _clean_value(row["title"]),
            "ctr_feed": _clean_value(row["ctr_feed"]),
            "reason": f"CTR Ленты > {CTR_FEED_ANOMALY_THRESHOLD}% — вероятно нет трейлера",
        }
        for _, row in anomalies.iterrows()
    ]


def _records_from_df(
    df: pd.DataFrame,
    fields: list[str],
    shelf: str,
    lowered: bool = False,
) -> list[dict]:
    records = []

    for _, row in df.iterrows():
        record = {
            "title": _clean_value(row["title"]),
        }

        for field in fields:
            record[field] = _clean_value(row.get(field))

        note = _build_note(row, shelf=shelf, lowered=lowered)

        if note:
            record["note"] = note

        records.append(record)

    return records


def _rating_records_from_df(df: pd.DataFrame) -> list[dict]:
    records = []

    for _, row in df.iterrows():
        note_parts = []

        if row.get("rotation_penalty", 1) < 1:
            penalty_percent = int((1 - row["rotation_penalty"]) * 100)
            note_parts.append(f"♻️ -{penalty_percent}% штраф за ротацию")

        if row.get("freshness_boost", 1) > 1:
            note_parts.append("🆕 +15% буст")

        if row.get("flag_small_views"):
            note_parts.append("⚠️ Малая выборка")

        records.append(
            {
                "title": _clean_value(row["title"]),
                "rating": int(row["rating"]),
                "base_score": _clean_value(row["base_score"]),
                "rating_score": _clean_value(row["rating_score"]),
                "rotation_penalty": _clean_value(row["rotation_penalty"]),
                "freshness_boost": _clean_value(row["freshness_boost"]),
                "note": "; ".join(note_parts),
            }
        )

    return records


def _build_note(row: pd.Series, shelf: str, lowered: bool = False) -> str:
    notes = []

    if row.get("anomaly_ctr_feed") and shelf in ("hot", "carousel"):
        notes.append("⚠️ CTR Ленты аномален")

    if row.get("flag_small_views"):
        notes.append("⚠️ Малая выборка")

    if row.get("flag_classic"):
        notes.append("📽 Классика — проверить релевантность")

    if lowered:
        if shelf == "carousel" and row.get("carousel_impressions", 0) < MIN_CAROUSEL_IMPRESSIONS:
            notes.append("📉 Пониженный порог показов")

        if shelf == "hot" and row.get("feed_impressions", 0) < MIN_FEED_IMPRESSIONS:
            notes.append("📉 Пониженный порог показов в ленте")

        if shelf == "top10" and row.get("views", 0) < MIN_VIEWS_TOP10:
            notes.append("📉 Пониженный порог просмотров")

    return "; ".join(notes)


def _build_warnings(shelves: dict) -> list[str]:
    warnings = []

    if shelves.get("lowered_carousel"):
        warnings.append("Карусель: применен пониженный порог показов")

    if shelves.get("lowered_top10"):
        warnings.append("Top 10: применен пониженный порог просмотров")

    if shelves.get("lowered_hot"):
        warnings.append("Hot: применен пониженный порог показов в ленте")

    return warnings


def _clean_value(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if hasattr(value, "item"):
        value = value.item()

    if isinstance(value, float):
        return round(value, 4)

    return value