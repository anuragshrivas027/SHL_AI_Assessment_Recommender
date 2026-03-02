from fastapi import FastAPI
from pydantic import BaseModel
from src.recommender import SHLRecommender

app = FastAPI()

# Load recommender once (important for performance)
recommender = SHLRecommender("data/shl_catalogue_cleaned.csv")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 10

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend")
def recommend_tests(request: QueryRequest):
    results = recommender.recommend(request.query, top_k=request.top_k)

    response = []

    for _, row in results.iterrows():
        response.append({
            "name": row["name"],
            "url": row["url"],
            "test_type": row["test_type"],
            "score": float(row["score"])
        })

    return {"recommendations": response}