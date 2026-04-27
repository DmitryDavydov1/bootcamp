from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"

# Минимальные пороги
MIN_CAROUSEL_IMPRESSIONS = 100
MIN_FEED_IMPRESSIONS = 20
MIN_VIEWS_TOP10 = 50
MIN_VIEWS_SMALL_SAMPLE = 30
CTR_FEED_ANOMALY_THRESHOLD = 50

# Пониженные пороги
MIN_CAROUSEL_IMPRESSIONS_LOW = 30
MIN_FEED_IMPRESSIONS_LOW = 5
MIN_VIEWS_TOP10_LOW = 20

# Минимальное число кандидатов перед снижением порогов
MIN_CANDIDATES_CAROUSEL = 8
MIN_CANDIDATES_TOP10 = 8
MIN_CANDIDATES_HOT = 8

# Размеры подборок
N_CAROUSEL = 15
N_TOP10 = 15
N_HOT = 20
N_RATING = 20

# Веса формул
CAROUSEL_WEIGHTS = {
    "ctr_carousel": 0.35,
    "views": 0.25,
    "depth": 0.20,
    "bwr": 0.20,
}

TOP10_WEIGHTS = {
    "views": 0.40,
    "total_time": 0.30,
    "depth": 0.20,
    "bwr": 0.10,
}

HOT_WEIGHTS = {
    "ctr_feed": 0.35,
    "source_feed": 0.25,
    "bwr": 0.25,
    "views": 0.15,
}

RATING_WEIGHTS = {
    "ctr_feed": 0.30,
    "ctr_carousel": 0.20,
    "views": 0.20,
    "bwr": 0.15,
    "depth": 0.10,
    "source_feed": 0.05,
}

ROTATION_PENALTY = {
    4: 0.85,
    6: 0.70,
}

FRESHNESS_BOOST = 1.15

BOSS_KEYWORDS = [
    "босс",
    "директор",
    "миллиардер",
    "начальник",
    "ceo",
    "шеф",
]

CLASSIC_KEYWORDS = [
    "броненосец",
    "волга",
    "весёлые ребята",
    "садко",
    "цирк",
    "свинарка",
    "подкидыш",
    "тимур",
    "белый клык",
    "небесный тихоход",
    "шофер",
    "каменный цветок",
    "дети капитана",
]