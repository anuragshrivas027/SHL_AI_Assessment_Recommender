import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.recommender import SHLRecommender

app = FastAPI(title="SHL Assessment Recommendation API")

# Load recommender once at startup
recommender = SHLRecommender("data/shl_master_dataset.csv")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 10


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/recommend")
def recommend_tests(request: QueryRequest):

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Enforce bounds as per assignment (1 to 10)
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
            for t in raw_types.split(",")
            if t.strip()
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
            "url": str(row["url"]),
            "name": str(row["name"]),
            "adaptive_support": "Yes" if str(row.get("adaptive_support")).strip().lower() == "yes" else "No",
            "description": "" if pd.isna(row.get("description")) else str(row.get("description")),
            "duration": duration_value,
            "remote_support": "Yes" if str(row.get("remote_support")).strip().lower() == "yes" else "No",
            "test_type": mapped_types
        })

    return {"recommended_assessments": response}