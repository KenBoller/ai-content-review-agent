import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from graph.workflow import graph


st.set_page_config(
    page_title="AI Content Review Agent",
    page_icon="📝",
    layout="wide",
)

st.title("AI Content Review Agent")
st.caption("LangGraph-powered content review workflow using local Ollama or Anthropic.")

article = st.text_area(
    "Paste article content",
    height=300,
    placeholder="Paste a blog post, landing page draft, or support article here...",
)

if st.button("Review Article"):
    if not article.strip():
        st.warning("Paste an article first.")
    else:
        with st.spinner("Reviewing article..."):
            result = graph.invoke({"article": article})

        st.subheader("Grammar Review")
        st.write(result.get("grammar_feedback", ""))

        st.subheader("SEO Review")
        st.write(result.get("seo_feedback", ""))

        st.subheader("Readability Review")
        st.write(result.get("readability_feedback", ""))

        st.subheader("Improved Article")
        st.text_area(
            "Rewritten Content",
            value=result.get("improved_article", ""),
            height=300,
        )

        with st.expander("Raw LangGraph State"):
            st.json(result)