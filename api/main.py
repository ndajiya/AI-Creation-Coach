from fastapi import FastAPI
from pydantic import BaseModel, Field
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from rag.engine import AnimeRAGEngine

app = FastAPI(title="Anime Creation Coach API", version="0.1.0")
engine = AnimeRAGEngine(str(ROOT / "data" / "anime_sample.csv"))

class ConceptRequest(BaseModel):
    concept: str = Field(..., min_length=3)
    k: int = Field(5, ge=1, le=10)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/concept/analyze")
def analyze(req: ConceptRequest):
    return engine.score_concept(req.concept, k=req.k)

@app.post("/concept/similar-anime")
def similar(req: ConceptRequest):
    return {"matches": engine.retrieve(req.concept, k=req.k)}
