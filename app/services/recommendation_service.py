from app.services.dataset_service import load_dataset
from app.recommendation_engine.anomalies import detect_anomalies
from app.recommendation_engine.shelves import build_unique_shelves


def generate_recommendations():
    titles_df, ctr_df = load_dataset()

    df = titles_df.copy()

    if ctr_df is not None:
        df = df.merge(ctr_df, on="title", how="left")

    df = df.fillna(0)

    # engine pipeline
    df = detect_anomalies(df)
    shelves = build_unique_shelves(df)

    carousel = [
        {
            "title": item["title"],
            "ctr_carousel": item["ctr_carousel"],
            "views": item["views"],
            "bwr": item["bwr"],
            "carousel_score": item["carousel_score"]
        }
        for item in shelves["carousel"].to_dict("records")
    ]
    top10 = [
        {
            "title": item["title"],
            "views": item["views"],
            "depth": item["depth"],
            "bwr": item["bwr"],
            "top10_score": item["top10_score"]
        }
        for item in shelves["top10"].to_dict("records")
    ]
    hot = [
        {
            "title": item["title"],
            "ctr_feed": item["ctr_feed"],
            "source_feed": item["source_feed"],
            "bwr": item["bwr"],
            "views": item["views"],
            "hot_score": item["hot_score"]
        }
        for item in shelves["hot"].to_dict("records")
    ]

    return {
        "carousel": carousel,
        "top10": top10,
        "hot": hot,
    }
