import pandas as pd
from src.recommender import SHLRecommender

def generate_predictions(input_excel, output_csv, k=10):
    # Load recommender
    recommender = SHLRecommender("data/shl_master_dataset.csv")

    # Load test set
    df = pd.read_excel(input_excel)

    rows = []

    for _, row in df.iterrows():
        query = row["Query"]

        results = recommender.recommend(query, top_k=k)

        for _, rec in results.iterrows():
            rows.append({
                "Query": query,
                "Assessment_url": rec["url"]
            })

    # Save to required submission format
    submission_df = pd.DataFrame(rows)
    submission_df.to_csv(output_csv, index=False)

    print(f"Submission file saved as {output_csv}")


if __name__ == "__main__":
    generate_predictions("Gen_AI_Dataset.xlsx", "test_predictions.csv", k=10)