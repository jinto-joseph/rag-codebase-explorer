"""Streamlit web application for RAG Codebase Explorer.

Provides a user-friendly interface for loading GitHub repositories,
compressing code files, and performing semantic code search using
natural language queries.

Usage:
    streamlit run app.py
"""

import streamlit as st
from repo_loader import load_repo
from compressor import compress, count_tokens
from rag import CodeRAG

st.title("RAG Codebase Explorer")

path = st.text_input("Enter path to a GitHub repo folder")

if st.button("Load Repo"):
    files = load_repo(path)
    st.write("Files found:", len(files))

    processed = []

    for f in files:
        compressed = compress(f["code"])
        processed.append({
            "path": f["path"],
            "original_tokens": count_tokens(f["code"]),
            "compressed_tokens": count_tokens(compressed),
            "compressed": compressed
        })

    rag = CodeRAG()
    rag.add(processed)
    st.session_state["rag"] = rag
    st.session_state["data"] = processed
    st.success(f"Loaded {len(processed)} files")

query = st.text_input("Ask about the code")

if st.button("Search"):
    results = st.session_state["rag"].query(query)
    for r in results:
        st.markdown(f"### {r['path']}")
        st.text(r["compressed"])
        st.write("Tokens:", r["original_tokens"], "→", r["compressed_tokens"])
