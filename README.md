# SHL AI Assessment Recommendation System

## Project Overview

This project is an AI-powered SHL assessment recommendation system built using FastAPI and Sentence Transformers. 
The system recommends relevant SHL Individual Test Solutions based on natural language job descriptions using semantic search.

Instead of relying on keyword matching, the system understands the context and intent of job descriptions by converting 
text into vector embeddings and performing similarity-based retrieval.

The project includes data crawling, dataset cleaning, embedding-based ranking, evaluation using Mean Recall@K, 
a REST API backend, an interactive Streamlit frontend, and live cloud deployment.


## Problem Statement

Recruiters often depend on manual filtering or keyword search to select assessments. 
Keyword-based systems fail to capture deeper contextual meaning and frequently return irrelevant results.

This project solves the problem by:

- Understanding complete job descriptions using transformer-based embeddings
- Matching them semantically with SHL assessment descriptions
- Returning structured and balanced recommendations
- Measuring retrieval performance using standard evaluation metrics
- Deploying the solution as a publicly accessible production API


## Data Collection and Preparation

The SHL product catalogue was crawled and processed to create a structured dataset.

Steps performed:

- Crawled SHL catalogue pages
- Excluded pre-packaged job solutions
- Collected 518 total assessments
- Cleaned and filtered to 415 usable Individual Test Solutions
- Structured important attributes:
  - name
  - url
  - description
  - test_type
  - duration
  - adaptive_support
  - remote_support

The final dataset is stored locally to ensure reproducibility and faster inference.


## System Architecture

Data Crawling → Data Cleaning → Dataset Structuring → Embedding Generation → Semantic Search → 
Balanced Ranking → API → Frontend → Cloud Deployment

The architecture is modular and organized inside the src directory with clear separation of concerns.


## Recommendation Engine

The system uses the sentence-transformers model: all-MiniLM-L6-v2

Process:

1. Convert all assessment descriptions into embeddings.
2. Convert the user query (job description) into an embedding.
3. Compute cosine similarity between query and assessment embeddings.
4. Retrieve top K most similar assessments.
5. Apply balancing logic across assessment categories.

This enables contextual matching rather than simple keyword overlap.


## Balanced Recommendation Strategy

To prevent dominance of a single assessment category, the system ensures diversity across domains such as:

- Knowledge & Skills
- Personality & Behavior
- Ability & Aptitude
- Simulations
- Competencies
- Assessment Exercises

This produces realistic and well-rounded recommendations aligned with job requirements.


## Evaluation

The model was evaluated using the provided labeled dataset.

Metric Used:
Mean Recall@K

Recall@K = Relevant results retrieved in Top K / Total relevant results

Performance progression:

Initial baseline:
Mean Recall@10 = 0.0200

After optimization:
Mean Recall@10 = 0.1467

With K = 20:
Mean Recall@20 = 0.2189

This improvement demonstrates effective preprocessing, ranking refinement, and embedding-based retrieval.

To run evaluation:

python -m src.evaluate


## API Implementation

The backend is implemented using FastAPI and deployed on Railway (Cloud).

Health Endpoint:
GET /health

Response:
{"status": "ok"}

Recommendation Endpoint:
POST /recommend

Input:

{
  "query": "Job description text",
  "top_k": 10
}

The API returns structured JSON containing recommended assessments with metadata.

### Running Locally

Start the FastAPI server:

python -m uvicorn app:app --port 8001

Then open:

http://127.0.0.1:8001/docs


## Live Deployment

The backend API is successfully deployed on Railway.

Public API Base URL:

https://shlaiassessmentrecommender-production.up.railway.app

Health Endpoint:

https://shlaiassessmentrecommender-production.up.railway.app/health

Recommendation Endpoint:

https://shlaiassessmentrecommender-production.up.railway.app/recommend

API Documentation:

https://shlaiassessmentrecommender-production.up.railway.app/docs

The service is publicly accessible and production-ready.


## Web Application (Frontend)

A Streamlit-based frontend provides an interactive interface where users can:

- Paste job descriptions
- Select number of recommendations
- View structured results

Live Web Application:

https://shlaiassessmentrecommender-production-1835.up.railway.app

To run locally:

streamlit run frontend.py


## Submission File Generation

To generate predictions for the test dataset:

python -m src.generate_test_predictions

This creates the final submission file:

anurag_shrivas.csv

Format:

Query,Assessment_url


## Tech Stack

Backend:
- FastAPI
- Uvicorn

Machine Learning:
- Sentence Transformers
- Scikit-learn (Cosine Similarity)
- PyTorch (CPU)

Data Processing:
- Pandas

Frontend:
- Streamlit

Deployment:
- Railway


## Project Structure

app.py  
frontend.py  
requirements.txt  
runtime.txt  
README.md  
approach_document.pdf  
anurag_shrivas.csv  

src/  
  - recommender.py  
  - evaluate.py  
  - generate_test_predictions.py  
  - crawler.py  
  - clean_catalog.py  
  - merge_datasets.py  
  - enrich_catalog.py  

data/  
  - shl_master_dataset.csv  

screenshots/  


## Key Highlights

- Semantic search instead of keyword filtering
- Balanced multi-category recommendations
- Measurable evaluation using Recall@K
- Modular and maintainable architecture
- REST API with structured responses
- Interactive frontend interface
- Reproducible dataset pipeline
- Live cloud deployment on Railway


## Author

Developed as part of SHL AI Internship Assignment by:

Anurag Shrivas

GitHub: https://github.com/anuragshrivas027  
LinkedIn: https://linkedin.com/in/anuragshrivas027