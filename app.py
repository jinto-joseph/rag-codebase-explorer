"""Streamlit web application for RAG Codebase Explorer.

Provides a user-friendly interface for loading GitHub repositories,
compressing code files, and performing semantic code search using
natural language queries.

Features Code Memory Mode: Remembers previous queries and reuses
context for multi-turn conversations with the codebase.

Usage:
    streamlit run app.py
"""

import streamlit as st
from repo_loader import load_repo
from compressor import compress, count_tokens
from rag import CodeRAG

st.title("🧠 RAG Codebase Explorer")

# Initialize Code Memory Mode
if "query_history" not in st.session_state:
    st.session_state["query_history"] = []
if "context_memory" not in st.session_state:
    st.session_state["context_memory"] = []

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
    # Reset memory when loading new repo
    st.session_state["query_history"] = []
    st.session_state["context_memory"] = []
    st.success(f"✅ Loaded {len(processed)} files")

query = st.text_input("Ask about the code")

# Show memory status
if st.session_state.get("query_history"):
    with st.expander("🧠 Code Memory Active (click to view history)"):
        st.write(f"**Previous queries:** {len(st.session_state['query_history'])}")
        for i, prev_q in enumerate(st.session_state["query_history"][-3:], 1):
            st.text(f"{i}. {prev_q}")
        if st.button("Clear Memory"):
            st.session_state["query_history"] = []
            st.session_state["context_memory"] = []
            st.success("Memory cleared!")

if st.button("Search"):
    # CODE MEMORY MODE: Build context-aware query
    enhanced_query = query
    if st.session_state["context_memory"]:
        # Combine current query with previous context (last 2 queries)
        recent_context = " ".join(st.session_state["context_memory"][-2:])
        enhanced_query = f"{recent_context} {query}"
        st.info(f"🧠 Using memory from {len(st.session_state['query_history'])} previous queries")
    
    results = st.session_state["rag"].query(enhanced_query)
    
    # Update memory
    st.session_state["query_history"].append(query)
    # Store relevant file paths as context for next query
    context_files = [r['path'] for r in results]
    st.session_state["context_memory"].append(f"Previously searched: {', '.join(context_files[:2])}")
    
    # Keep memory manageable (last 5 queries)
    if len(st.session_state["query_history"]) > 5:
        st.session_state["query_history"] = st.session_state["query_history"][-5:]
        st.session_state["context_memory"] = st.session_state["context_memory"][-5:]
    
    for r in results:
        st.markdown(f"### 📄 {r['path']}")
        st.code(r["compressed"], language="python")
        st.caption(f"Tokens: {r['original_tokens']} → {r['compressed_tokens']} (reduction: {100 - int(r['compressed_tokens']/r['original_tokens']*100)}%)")
