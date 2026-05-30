"""
MCP-style tool layer stub.

This is not a full MCP server yet. It isolates the tool functions you would expose
to an MCP host such as Claude Desktop, Cursor, or your own agent runtime.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from rag.engine import AnimeRAGEngine

engine = AnimeRAGEngine(str(ROOT / "data" / "anime_sample.csv"))

def analyze_anime_concept(concept: str, k: int = 5) -> dict:
    """Return RAG-based market-fit, closest anime parallels, and creative guidance."""
    return engine.score_concept(concept, k=k)

def find_similar_anime(concept: str, k: int = 5) -> dict:
    """Return the closest anime records for a concept."""
    return {"matches": engine.retrieve(concept, k=k)}
