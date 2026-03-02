SHL AI Assessment Recommendation System
Overview

This project is an AI-powered assessment recommendation system designed to recommend relevant SHL Individual Test Solutions based on natural language job descriptions.

The system uses semantic search with sentence embeddings to understand job requirements and retrieve the most relevant assessments from the SHL product catalogue.

It supports:

Semantic similarity-based retrieval

Balanced recommendations across multiple test types

Evaluation using Mean Recall@K

REST API using FastAPI

Interactive frontend using Streamlit

Reproducible dataset preparation pipeline

Problem Statement

Recruiters often rely on keyword-based filtering to select assessments, which leads to poor relevance and lack of contextual understanding.

This system addresses that limitation by:

Understanding full job descriptions

Matching them semantically to assessment descriptions

Returning structured, domain-balanced recommendations

Measuring retrieval performance using standard metrics

System Architecture

The solution follows a modular pipeline:

Data Crawling → Cleaning → Dataset Preparation → Embedding Generation → Semantic Retrieval → Balanced Ranking → API → Frontend

Project Structure
SHL_AI_Project/
│
├── app.py
├── frontend.py
├── requirements.txt
├── README.md
├── approach_document.pdf
├── test_predictions.csv
│
├── src/
│   ├── recommender.py
│   ├── evaluate.py
│   ├── generate_test_predictions.py
│   ├── crawler.py
│   ├── clean_catalog.py
│   ├── merge_datasets.py
│   └── enrich_catalog.py
│
├── data/
│   └── shl_master_dataset.csv
│
└── screenshots/
Data Preparation

Crawled SHL product catalogue.

Excluded Pre-packaged Job Solutions.

Collected 518 total assessments.

Cleaned and filtered to 415 usable Individual Test Solutions.

Stored the following attributes:

name

url

description

test_type

duration

adaptive_support

remote_support

All data is stored locally to ensure reproducibility.

Recommendation Engine

The system uses:

sentence-transformers (all-MiniLM-L6-v2)

Cosine similarity for semantic search

Steps:

Convert assessment descriptions into embeddings.

Convert user query into embedding.

Compute cosine similarity.

Retrieve top K most similar assessments.

Apply balancing logic across test types.

This allows contextual understanding rather than keyword matching.

Balanced Recommendation Strategy

To prevent dominance of a single assessment category, the system:

Uses test_type metadata

Ensures diversity across:

Knowledge & Skills

Personality & Behavior

Ability & Aptitude

Simulations

Competencies

Assessment Exercises

This ensures realistic and well-rounded recommendations.

Evaluation

Evaluation was performed using the provided labeled dataset.

Metric Used:

Mean Recall@K

Recall@K = Relevant Retrieved in Top K / Total Relevant

Performance Improvements:

Initial baseline:
Mean Recall@10 = 0.0200

After optimization:
Mean Recall@10 = 0.1467

With K = 20:
Mean Recall@20 = 0.2189

This demonstrates measurable improvement through preprocessing and ranking enhancements.

To run evaluation:

python -m src.evaluate
API Implementation

Built using FastAPI.

Health Check

GET /health

Response:

{
  "status": "ok"
}
Recommendation Endpoint

POST /recommend

Input:

{
  "query": "Job description text",
  "top_k": 10
}

Output:

{
  "recommended_assessments": [
    {
      "url": "...",
      "name": "...",
      "adaptive_support": "Yes/No",
      "description": "...",
      "duration": 45,
      "remote_support": "Yes/No",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}

To run API locally:

uvicorn app:app --reload

Then open:

http://127.0.0.1:8000/docs
Frontend

A Streamlit-based interface allows users to:

Paste job descriptions

Adjust number of recommendations

View structured output interactively

To run locally:

streamlit run frontend.py
Generating Submission File

To generate predictions for the test dataset:

python -m src.generate_test_predictions

This creates:

test_predictions.csv

Format:

Query,Assessment_url
Installation

Create virtual environment:

python -m venv venv
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Dependencies

fastapi

uvicorn

pandas

sentence-transformers

scikit-learn

streamlit

Deployment

The application can be deployed using:

Render

Railway

HuggingFace Spaces

Start command for API:

uvicorn app:app --host 0.0.0.0 --port 10000

Start command for Streamlit:

streamlit run frontend.py --server.port 10000 --server.address 0.0.0.0
Key Highlights

Fully modular pipeline

Semantic search instead of keyword filtering

Balanced recommendation logic

Measurable evaluation

Clean API design

Interactive frontend

Reproducible workflow

Author

Developed as part of SHL AI Internship Assignment
Candidate: Anurag Shrivas
