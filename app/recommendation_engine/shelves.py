import pandas as pd

from app.recommendation_engine.scoring import calc_scores
from app.recommendation_engine.config import (
    MIN_FEED_IMPRESSIONS,
    MIN_FEED_IMPRESSIONS_LOW,
    MIN_VIEWS_TOP10,
    MIN_VIEWS_TOP10_LOW,
    MIN_CANDIDATES_CAROUSEL,
    MIN_CANDIDATES_TOP10,
    MIN_CANDIDATES_HOT,
    N_CAROUSEL,
    N_TOP10,
    N_HOT,
)


def build_unique_shelves(df: pd.DataFrame) -> dict:
    """
    Формирует три подборки без пересечений.
    Приоритет: Карусель → Top 10 → Hot.
    Возвращает словарь с DataFrames и флагами снижения порогов.
    """
    used: set = set()
    result = {}

    # ── КАРУСЕЛЬ ─────────────────────────────────────────────────────────────
    lowered_carousel = False
    df_car = calc_scores(df)
    candidates_car = (df_car[~df_car["title"].isin(used)]
                      .sort_values("carousel_score", ascending=False))
    if len(candidates_car) < MIN_CANDIDATES_CAROUSEL:
        # Снижаем порог показов карусели
        df_car = calc_scores(df)
        candidates_car = (df_car[~df_car["title"].isin(used)]
                          .sort_values("carousel_score", ascending=False))
        lowered_carousel = True

    carousel_df = candidates_car.head(N_CAROUSEL).reset_index(drop=True)
    carousel_df.index += 1
    used.update(carousel_df["title"].tolist())
    result["carousel"] = carousel_df
    result["lowered_carousel"] = lowered_carousel
    # Сохраняем версию df с пересчитанными скорами для дальнейших подборок
    df_scored = df_car.copy()

    # ── TOP 10 ───────────────────────────────────────────────────────────────
    lowered_views = False
    min_views = MIN_VIEWS_TOP10
    candidates_top = (df_scored[
                          (~df_scored["title"].isin(used)) &
                          (df_scored["views"] >= min_views)
                          ].sort_values("top10_score", ascending=False))

    if len(candidates_top) < MIN_CANDIDATES_TOP10:
        min_views = MIN_VIEWS_TOP10_LOW
        candidates_top = (df_scored[
                              (~df_scored["title"].isin(used)) &
                              (df_scored["views"] >= min_views)
                              ].sort_values("top10_score", ascending=False))
        lowered_views = True

    top10_df = candidates_top.head(N_TOP10).reset_index(drop=True)
    top10_df.index += 1
    used.update(top10_df["title"].tolist())
    result["top10"] = top10_df
    result["lowered_top10"] = lowered_views

    # ── HOT ──────────────────────────────────────────────────────────────────
    lowered_feed = False
    min_feed = MIN_FEED_IMPRESSIONS
    candidates_hot = df_scored[
        (~df_scored["title"].isin(used)) &
        (df_scored["ctr_feed"] > 0) &
        (~df_scored["anomaly_ctr_feed"]) &
        (df_scored["feed_impressions"] >= min_feed)
        ].sort_values("hot_score", ascending=False)

    if len(candidates_hot) < MIN_CANDIDATES_HOT:
        min_feed = MIN_FEED_IMPRESSIONS_LOW
        candidates_hot = df_scored[
            (~df_scored["title"].isin(used)) &
            (df_scored["ctr_feed"] > 0) &
            (~df_scored["anomaly_ctr_feed"]) &
            (df_scored["feed_impressions"] >= min_feed)
            ].sort_values("hot_score", ascending=False)
        lowered_feed = True

    hot_df = candidates_hot.head(N_HOT).reset_index(drop=True)
    hot_df.index += 1
    result["hot"] = hot_df
    result["lowered_hot"] = lowered_feed
    result["df_scored"] = df_scored

    return result
