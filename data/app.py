import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from src.recommender import SHLRecommender

app = FastAPI(
    title="SHL AI Assessment Recommendation API",
    description="API that recommends relevant SHL assessments based on natural language job descriptions using semantic search.",
    version="1.0"
)

# Load recommender once (important for performance)
recommender = SHLRecommender("data/shl_master_dataset.csv")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 10


# Root endpoint (for base URL)
@app.get("/")
def root():
    return {
        "message": "SHL AI Assessment Recommendation API is running",
        "documentation": "/docs",
        "health_check": "/health",
        "recommendation_endpoint": "/recommend"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Recommendation endpoint
@app.post("/recommend")
def recommend_tests(request: QueryRequest):

    results = recommender.recommend(request.query, top_k=request.top_k)

    response = []

    for _, row in results.iterrows():

        type_mapping = {
            "K": "Knowledge & Skills",
            "P": "Personality & Behavior",
            "A": "Ability & Aptitude",
            "C": "Competencies",
            "E": "Assessment Exercises",
            "S": "Simulations",
            "D": "Development & 360"
        }

        raw_types = str(row.get("test_type", ""))
        mapped_types = [
            type_mapping.get(t.strip(), t.strip())
            for t in raw_types.split(",") if t.strip()
        ]

        response.append({
            "url": str(row["url"]),
            "name": str(row["name"]),
            "adaptive_support": "Yes" if str(row.get("adaptive_support")).lower() == "yes" else "No",
            "description": "" if pd.isna(row.get("description")) else str(row.get("description")),
            "duration": int(row.get("duration")) if str(row.get("duration")).isdigit() else 0,
            "remote_support": "Yes" if str(row.get("remote_support")).lower() == "yes" else "No",
            "test_type": mapped_types
        })

    return {"recommended_assessments": response}