import streamlit as st
import pandas as pd
from rag.engine import AnimeRAGEngine

st.set_page_config(page_title="Anime Creation Coach", page_icon="🎬", layout="wide")

@st.cache_resource
def load_engine():
    return AnimeRAGEngine("data/anime_sample.csv")

engine = load_engine()

st.title("🎬 Anime Creation Coach")
st.caption("RAG-powered market-fit and creative positioning prototype for anime concepts.")

concept = st.text_area(
    "Describe your anime concept",
    "A high-stakes virtual reality space opera where trapped players govern a starship civilization through game rules.",
    height=120,
)
k = st.slider("Number of parallels to retrieve", 3, 10, 5)

if st.button("Analyze concept", type="primary"):
    result = engine.score_concept(concept, k=k)

    c1, c2, c3 = st.columns(3)
    c1.metric("Concept Score", f"{result['concept_score']}/100")
    c2.metric("Estimated Popularity", result["estimated_popularity"])
    c3.metric("Estimated Rating", result["estimated_rating"])

    st.subheader("Creative Coach")
    st.write(result["summary"])

    st.subheader("Top Signal Tags")
    st.dataframe(pd.DataFrame(result["top_tags"].items(), columns=["Tag", "Frequency"]), use_container_width=True)

    st.subheader("Closest Anime Parallels")
    rows = []
    for m in result["matches"]:
        rows.append({
            "Title": m["title"],
            "Similarity": m["similarity"],
            "Popularity": m["popularity"],
            "Score": m["score"],
            "Tags": m["tags"],
            "Recommendations": m["recommendations"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("Synopsis Improvement Prompt")
    st.code(
        "Rewrite this anime concept into 3 market-tested synopsis variants using the strongest tags, "
        "closest parallels, and an original twist. Avoid copying any existing anime.",
        language="text",
    )
else:
    st.info("Enter a concept and click Analyze concept.")
