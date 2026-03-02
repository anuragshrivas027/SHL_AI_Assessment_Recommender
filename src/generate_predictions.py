import pandas as pd
from src.recommender import SHLRecommender


def generate_predictions(excel_file, output_file, k=10):

    print("Loading Test-Set...")
    df = pd.read_excel(excel_file, sheet_name="Test-Set")

    recommender = SHLRecommender("data/shl_master_dataset.csv")

    rows = []

    for _, row in df.iterrows():
        query = row["Query"]

        recommendations = recommender.recommend(query, top_k=k)

        for _, rec in recommendations.iterrows():
            rows.append({
                "Query": query,
                "Assessment_url": rec["url"]
            })

    result_df = pd.DataFrame(rows)

    result_df.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")


if __name__ == "__main__":
    generate_predictions("Gen_AI_Dataset.xlsx", "data/final_predictions.csv", k=10)