import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.recommender import SHLRecommender

# Initialize FastAPI app
app = FastAPI(
    title="SHL AI Assessment Recommendation API",
    description="API that recommends relevant SHL assessments based on natural language job descriptions using semantic search.",
    version="1.0"
)

# Load recommender (once at startup)
try:
    recommender = SHLRecommender("data/shl_master_dataset.csv")
except Exception as e:
    recommender = None
    print("Error loading recommender:", e)


# Request schema
class QueryRequest(BaseModel):
    query: str
    top_k: int = 10


# Root endpoint (fix for base URL)
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

    if recommender is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        results = recommender.recommend(request.query, top_k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response = []

    type_mapping = {
        "K": "Knowledge & Skills",
        "P": "Personality & Behavior",
        "A": "Ability & Aptitude",
        "C": "Competencies",
        "E": "Assessment Exercises",
        "S": "Simulations",
        "D": "Development & 360"
    }

    for _, row in results.iterrows():

        raw_types = str(row.get("test_type", ""))
        mapped_types = [
            type_mapping.get(t.strip(), t.strip())
            for t in raw_types.split(",") if t.strip()
        ]

        response.append({
            "url": str(row.get("url", "")),
            "name": str(row.get("name", "")),
            "adaptive_support": "Yes" if str(row.get("adaptive_support", "")).lower() == "yes" else "No",
            "description": "" if pd.isna(row.get("description")) else str(row.get("description")),
            "duration": int(row.get("duration")) if str(row.get("duration")).isdigit() else 0,
            "remote_support": "Yes" if str(row.get("remote_support", "")).lower() == "yes" else "No",
            "test_type": mapped_types
        })

    return {"recommended_assessments": response}