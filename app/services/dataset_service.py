from pathlib import Path
import pandas as pd

UPLOAD_DIR = Path(__file__).parent.parent / "storage" / "uploads"


def find_file(prefix: str):
    files = list(UPLOAD_DIR.glob(f"*{prefix}*.csv"))
    return files[0] if files else None


def load_dataset():
    titles = UPLOAD_DIR / "title-kinolenta.csv"
    ctr = UPLOAD_DIR / "ctr-kinolenta.csv"

    titles_df = pd.read_csv(titles)
    ctr_df = pd.read_csv(ctr) if ctr else None

    titles_df = titles_df.rename(columns={
        "Тайтл": "title",
        "Количество просмотров": "views",
        "Общее время (ч.)": "total_time",
        "Количество платных просмотров": "paid_views",
        "Среднее время (сек)": "avg_watch_time",
        "Binge-Watch Rate": "bwr",
        "Средняя глубина просмотра тайтла (%)": "depth",

        "Источник: Главная (%)": "source_main",
        "Источник: Пуш (%)": "source_push",
        "Источник: Список эпизодов (%)": "source_episode_list",
        "Источник: Следующий эпизод (%)": "source_next_episode",
        "Источник: Диплинк (%)": "source_deeplink",
        "Источник: Лента (%)": "source_feed",
        "Источник: История (%)": "source_history",
        "Источник: Поиск (%)": "source_search",
        "Источник: Жанр (%)": "source_genre",
        "Источник: Избранное (%)": "source_favorites",
        "Источник: Карусель (%)": "source_carousel",
        "Источник: Внутри подборки (%)": "source_collection",
        "Источник: Каталог (%)": "source_catalog",
        "Источник: Предыдущий эпизод (%)": "source_prev_episode",

        "Retention 3 (%)": "retention_3",
        "Retention 5 (%)": "retention_5",
        "Retention 10 (%)": "retention_10",
        "Retention 15 (%)": "retention_15",
        "Retention 30 (%)": "retention_30",

        "Источник: Подборка (%)": "source_collection_inner",
        "Источник: Внутри карусели (%)": "source_carousel_inner",
    })

    ctr_df = ctr_df.rename(columns={
        "Тайтл": "title",
        "Карусель (%)": "ctr_carousel",
        "Лента (%)": "ctr_feed",
        "Кол-во показов в карусели": "carousel_impressions",
        "Кол-во просмотров в карусели": "carousel_views",
        "Кол-во показов в ленте": "feed_impressions",
        "Кол-во просмотров в ленте": "feed_views",
    })

    return titles_df, ctr_df
