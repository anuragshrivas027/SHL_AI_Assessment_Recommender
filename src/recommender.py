import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

class SHLRecommender:

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

        # Combine fields for embedding
        self.df["combined_text"] = (
            self.df["name"].fillna("") + " " +
            self.df["description"].fillna("") + " " +
            self.df["test_type"].fillna("")
        )

        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        print("Generating embeddings...")
        self.embeddings = self.model.encode(
            self.df["combined_text"].tolist(),
            show_progress_bar=True
        )

    def keyword_overlap_score(self, query, text):
        query_words = set(re.findall(r"\w+", query.lower()))
        text_words = set(re.findall(r"\w+", text.lower()))

        if not query_words:
            return 0

        return len(query_words & text_words) / len(query_words)

    def recommend(self, query, top_k=10):

        query_embedding = self.model.encode([query])
        cosine_scores = cosine_similarity(query_embedding, self.embeddings)[0]

        keyword_scores = self.df["combined_text"].apply(
            lambda text: self.keyword_overlap_score(query, text)
        ).values

        # Hybrid score
        final_scores = 0.6 * cosine_scores + 0.4 * keyword_scores

        self.df["score"] = final_scores

        results = self.df.sort_values(by="score", ascending=False).head(top_k)

        return results