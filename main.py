from src.recommender import SHLRecommender

def main():
    recommender = SHLRecommender("data/shl_catalogue_cleaned.csv")

    query = input("Enter job description or query: ")

    results = recommender.recommend(query)

    print("\nTop Recommendations:\n")
    print(results[["name", "url", "test_type", "score"]])

if __name__ == "__main__":
    main()