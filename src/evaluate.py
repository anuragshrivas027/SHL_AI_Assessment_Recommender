import pandas as pd
from src.recommender import SHLRecommender


def normalize_url(url):
    """
    Normalize URLs to ensure matching between
    train dataset and scraped dataset.
    """
    if pd.isna(url):
        return ""

    url = str(url).strip().lower().rstrip("/")

    # Remove '/solutions' if present (scraped URLs may include it)
    url = url.replace("/solutions", "")

    return url


def recall_at_k(recommended, relevant, k):
    """
    Compute Recall@K
    """
    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & set(relevant))
    return hits / len(relevant) if relevant else 0


def evaluate(excel_file, k=10):

    print("Loading train dataset...")
    df = pd.read_excel(excel_file, sheet_name="Train-Set")

    # Group ground truth URLs by Query
    grouped = df.groupby("Query")["Assessment_url"].apply(list).reset_index()

    print("Loading recommender...")
    recommender = SHLRecommender("data/shl_master_dataset.csv")

    recalls = []

    for _, row in grouped.iterrows():

        query = row["Query"]
        relevant_urls = row["Assessment_url"]

        # Normalize relevant URLs
        relevant_urls = [normalize_url(u) for u in relevant_urls]

        recommendations = recommender.recommend(query, top_k=k)

        recommended_urls = recommendations["url"].tolist()

        # Normalize recommended URLs
        recommended_urls = [normalize_url(u) for u in recommended_urls]

        recall = recall_at_k(recommended_urls, relevant_urls, k)
        recalls.append(recall)

    mean_recall = sum(recalls) / len(recalls)

    print(f"\nMean Recall@{k}: {mean_recall:.4f}")
    return mean_recall


if __name__ == "__main__":
    evaluate("Gen_AI_Dataset.xlsx", k=10)