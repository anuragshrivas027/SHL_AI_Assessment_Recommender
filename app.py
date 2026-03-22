import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.recommender import SHLRecommender

app = FastAPI(
    title="SHL AI Assessment Recommendation API",
    description="API that recommends relevant SHL assessments using semantic search.",
    version="1.0"
)

# Load recommender once
recommender = SHLRecommender("data/shl_master_dataset.csv")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 10


# ✅ ROOT ENDPOINT
@app.get("/")
def root():
    return {
        "message": "SHL AI Assessment Recommendation API is running",
        "docs": "/docs",
        "health": "/health",
        "recommend_usage": "Use POST /recommend with JSON body"
    }


# ✅ HEALTH CHECK
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ✅ GET SUPPORT FOR /recommend (to avoid Method Not Allowed)
@app.get("/recommend")
def recommend_info():
    return {
        "message": "This endpoint requires a POST request",
        "how_to_use": {
            "method": "POST",
            "endpoint": "/recommend",
            "body": {
                "query": "Java developer with 3 years experience",
                "top_k": 5
            }
        }
    }


# ✅ POST RECOMMENDATION (MAIN LOGIC)
@app.post("/recommend")
def recommend_tests(request: QueryRequest):

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Limit top_k between 1–10
    top_k = max(1, min(request.top_k, 10))

    results = recommender.recommend(request.query, top_k=top_k)

    if results.empty:
        raise HTTPException(status_code=404, detail="No assessments found")

    type_mapping = {
        "K": "Knowledge & Skills",
        "P": "Personality & Behavior",
        "A": "Ability & Aptitude",
        "C": "Competencies",
        "E": "Assessment Exercises",
        "S": "Simulations",
        "D": "Development & 360"
    }

    response = []

    for _, row in results.iterrows():

        raw_types = str(row.get("test_type", ""))
        mapped_types = [
            type_mapping.get(t.strip(), t.strip())
            for t in raw_types.split(",") if t.strip()
        ]

        # Clean duration
        duration_value = row.get("duration")
        if pd.isna(duration_value):
            duration_value = 0
        else:
            try:
                duration_value = int(duration_value)
            except:
                duration_value = 0

        response.append({
            "url": str(row.get("url", "")),
            "name": str(row.get("name", "")),
            "adaptive_support": "Yes" if str(row.get("adaptive_support", "")).strip().lower() == "yes" else "No",
            "description": "" if pd.isna(row.get("description")) else str(row.get("description")),
            "duration": duration_value,
            "remote_support": "Yes" if str(row.get("remote_support", "")).strip().lower() == "yes" else "No",
            "test_type": mapped_types
        })

    return {"recommended_assessments": response}