# Anime Creation Coach

A CPU-friendly prototype for an anime creation coach/API using RAG over anime metadata.

## What it does

- Accepts an anime concept.
- Retrieves similar anime using tags, synopsis, and recommendations.
- Scores the concept using weighted popularity and rating signals.
- Produces creative strategy guidance.
- Includes both a Streamlit UI and an HTML5 frontend backed by FastAPI.
- Includes an MCP-style tool layer stub for future agent integration.

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run Streamlit

```bash
streamlit run app.py
```

## Run the API

```bash
uvicorn api.main:app --reload --port 8000
```

Then open:

```txt
frontend/index.html
```

## Example API request

```bash
curl -X POST http://localhost:8000/concept/analyze \
  -H "Content-Type: application/json" \
  -d '{"concept":"high-stakes virtual reality space opera", "k":5}'
```

## How to upgrade it

1. Replace `data/anime_sample.csv` with a larger licensed dataset.
2. Add external IDs for Anime-Planet, AniList, MAL, Kitsu, etc.
3. Replace TF-IDF with sentence embeddings if your CPU can handle it.
4. Add a local LLM via Ollama, llama.cpp, or a hosted model for richer writing feedback.
5. Convert `mcp/anime_tools.py` into a full MCP server once your agent runtime is selected.

## Important note

Do not copy anime stories. The tool should recommend market positioning, audience overlap, and trope patterns, not generate derivative works that imitate protected expression.
