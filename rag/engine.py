from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class AnimeRAGEngine:
    data_path: str = "data/anime_sample.csv"

    def __post_init__(self) -> None:
        self.df = pd.read_csv(self.data_path)
        self.df["document"] = (
            self.df["title"].fillna("") + "\nTags: " + self.df["tags"].fillna("") +
            "\nSynopsis: " + self.df["synopsis"].fillna("") +
            "\nRecommendations: " + self.df["recommendations"].fillna("")
        )
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.df["document"].tolist())

    def retrieve(self, concept: str, k: int = 5) -> List[Dict[str, Any]]:
        query_vec = self.vectorizer.transform([concept])
        sims = cosine_similarity(query_vec, self.matrix).flatten()
        idxs = np.argsort(sims)[::-1][:k]
        results = []
        for idx in idxs:
            row = self.df.iloc[idx].to_dict()
            row["similarity"] = round(float(sims[idx]), 4)
            results.append(row)
        return results

    def score_concept(self, concept: str, k: int = 5) -> Dict[str, Any]:
        matches = self.retrieve(concept, k=k)
        if not matches:
            return {"concept_score": 0, "matches": [], "summary": "No matches found."}

        weights = np.array([max(m["similarity"], 0.01) for m in matches])
        popularity = np.array([float(m["popularity"]) for m in matches])
        score = np.array([float(m["score"]) for m in matches])
        weighted_popularity = float(np.average(popularity, weights=weights))
        weighted_score = float(np.average(score, weights=weights))

        concept_score = (weighted_popularity / 100 * 0.55) + (weighted_score / 10 * 0.45)
        concept_score = round(concept_score * 100, 1)

        tags = []
        for m in matches:
            tags.extend([t.strip() for t in str(m["tags"]).split(";")])
        tag_counts = pd.Series(tags).value_counts().head(8).to_dict()

        return {
            "concept": concept,
            "concept_score": concept_score,
            "estimated_popularity": round(weighted_popularity, 1),
            "estimated_rating": round(weighted_score, 2),
            "top_tags": tag_counts,
            "matches": matches,
            "summary": self._coach_response(concept, matches, tag_counts, concept_score),
        }

    def _coach_response(self, concept: str, matches: List[Dict[str, Any]], tag_counts: Dict[str, int], concept_score: float) -> str:
        titles = ", ".join([m["title"] for m in matches[:4]])
        tags = ", ".join(list(tag_counts.keys())[:6])
        return (
            f"Concept score: {concept_score}/100. This idea has useful overlap with {titles}. "
            f"The strongest market signals are: {tags}. "
            "To improve the pitch, make the core conflict specific, define the rules of the world, "
            "and show why the audience should care about the characters beyond the setting."
        )
