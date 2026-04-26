import pandas as pd
from pathlib import Path

from app.recommendation_engine.scoring import calc_scores

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
    df_car = calc_scores(df, carousel_imp_threshold=MIN_CAROUSEL_IMPRESSIONS)
    candidates_car = (df_car[~df_car["title"].isin(used)]
                      .sort_values("carousel_score", ascending=False))
    if len(candidates_car) < MIN_CANDIDATES_CAROUSEL:
        # Снижаем порог показов карусели
        df_car = calc_scores(df, carousel_imp_threshold=MIN_CAROUSEL_IMPRESSIONS_LOW)
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
