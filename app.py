"""Streamlit web application for RAG Codebase Explorer.

Provides a user-friendly interface for loading GitHub repositories
(from URL or local path), compressing code files, and performing 
semantic code search using natural language queries with AI-powered answers.

DEPLOYMENT READY: Works on Streamlit Cloud without file uploads!

Features Code Memory Mode: Remembers previous queries and reuses
context for multi-turn conversations with the codebase.

Usage:
    streamlit run app.py
"""

import streamlit as st
from repo_loader import load_repo, is_github_url
from compressor import compress, count_tokens
from rag import CodeRAG
import os

st.set_page_config(page_title="Code Navigator", page_icon="🧠", layout="wide")

st.title("🧠 Code Documentation Navigator")
st.markdown("*Powered by RAG + ScaleDown Compression*")

# Check API key status and show info banner
from config import get_gemini_api_key
_api_key = get_gemini_api_key()
if not _api_key:
    st.info("💡 **Tip:** Add a Gemini API key for AI-powered answers! The app works fine without it, showing retrieved code files. [Get a FREE key here](https://makersuite.google.com/app/apikey) and set as `GEMINI_API_KEY` environment variable.")

# Initialize session state
if "query_history" not in st.session_state:
    st.session_state["query_history"] = []
if "context_memory" not in st.session_state:
    st.session_state["context_memory"] = []
if "rag" not in st.session_state:
    st.session_state["rag"] = None
if "current_repo" not in st.session_state:
    st.session_state["current_repo"] = None

# Sidebar for repository loading
with st.sidebar:
    st.header("📂 Load Repository")
    
    input_type = st.radio(
        "Choose input method:",
        ["GitHub URL", "Local Path"],
        help="For Streamlit Cloud deployment, use GitHub URL"
    )
    
    if input_type == "GitHub URL":
        path = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repo",
            help="Enter the full GitHub repository URL"
        )
        st.caption("💡 Example: https://github.com/streamlit/streamlit")
    else:
        path = st.text_input(
            "Local Repository Path",
            placeholder="C:/path/to/repo",
            help="Enter the absolute path to a local repository"
        )
        st.caption("⚠️ Local paths won't work on Streamlit Cloud")
    
    load_button = st.button("🚀 Load Repository", use_container_width=True)
    
    if load_button and path:
        if not path.strip():
            st.error("Please enter a repository URL or path.")
        else:
            with st.spinner("Loading and processing repository..."):
                try:
                    # Load repository
                    files, repo_path = load_repo(path)
                    
                    if len(files) == 0:
                        st.error("No supported code files found in the repository.")
                    else:
                        st.info(f"Found {len(files)} files. Processing...")
                        
                        # Process and compress files
                        processed = []
                        progress_bar = st.progress(0)
                        
                        for idx, f in enumerate(files):
                            compressed = compress(f["code"])
                            processed.append({
                                "path": f["path"],
                                "original_tokens": count_tokens(f["code"]),
                                "compressed_tokens": count_tokens(compressed),
                                "compressed": compressed
                            })
                            progress_bar.progress((idx + 1) / len(files))
                        
                        # Build RAG index
                        rag = CodeRAG()
                        rag.add(processed)
                        
                        # Save to session state
                        st.session_state["rag"] = rag
                        st.session_state["data"] = processed
                        st.session_state["current_repo"] = path
                        st.session_state["query_history"] = []
                        st.session_state["context_memory"] = []
                        
                        # Calculate statistics
                        total_original = sum(f["original_tokens"] for f in processed)
                        total_compressed = sum(f["compressed_tokens"] for f in processed)
                        compression_ratio = (1 - total_compressed / total_original) * 100 if total_original > 0 else 0
                        
                        st.success(f"✅ Loaded {len(processed)} files")
                        st.metric("Compression", f"{compression_ratio:.1f}%", 
                                 help=f"{total_original} → {total_compressed} tokens")
                    
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"**Error loading repository:**")
                    st.error(error_msg)
                    
                    # Provide helpful suggestions based on error type
                    if "Access is denied" in error_msg or "WinError 5" in error_msg:
                        st.info("""
                        **💡 Windows Permission Error - Try these solutions:**
                        
                        1. **Close any file explorers** viewing the `temp_repos` folder
                        2. **Delete the temp_repos folder manually** and try again
                        3. **Try a different repository** to test if it's repo-specific
                        4. **Restart the app** - click the ⋮ menu → Rerun
                        """)
                    elif "Authentication failed" in error_msg or "not found" in error_msg:
                        st.info("""
                        **💡 Repository Access Error:**
                        
                        - Make sure the URL is correct and the repository is **public**
                        - Private repositories require authentication (not supported yet)
                        - Example: `https://github.com/streamlit/streamlit`
                        """)
                    elif "git" in error_msg.lower():
                        st.info("""
                        **💡 Git Error:**
                        
                        - Make sure Git is installed on your system
                        - Or try using a **Local Path** instead of GitHub URL
                        """)
    
    # Show current repository info
    if st.session_state.get("current_repo"):
        st.divider()
        st.caption(f"**Current Repo:**")
        st.caption(f"{st.session_state['current_repo']}")
        if st.button("Clear Repository"):
            st.session_state["rag"] = None
            st.session_state["data"] = None
            st.session_state["current_repo"] = None
            st.session_state["query_history"] = []
            st.session_state["context_memory"] = []
            st.rerun()
    
    # Cleanup utilities
    st.divider()
    st.caption("**Utilities**")
    if st.button("🧹 Clean Temp Files", help="Delete temporary cloned repositories"):
        try:
            from config import DEFAULT_CLONE_DIR
            import shutil
            if os.path.exists(DEFAULT_CLONE_DIR):
                shutil.rmtree(DEFAULT_CLONE_DIR, ignore_errors=True)
                st.success("✅ Temp files cleaned!")
            else:
                st.info("No temp files to clean")
        except Exception as e:
            st.warning(f"Cleanup warning: {str(e)}")

# Main area for querying
if st.session_state.get("rag") is None:
    st.info("👈 Start by loading a repository from the sidebar")
    
    with st.expander("💡 How to use"):
        st.markdown("""
        1. **Choose input method**: GitHub URL (recommended for deployment) or Local Path
        2. **Enter repository location** and click Load Repository
        3. **Wait for processing** - files will be compressed and indexed
        4. **Ask questions** about the codebase in natural language
        5. **Get AI-powered answers** with file references
        
        **Example queries:**
        - "Where is authentication handled?"
        - "Which files handle database queries?"
        - "Explain the main function"
        - "Find the API endpoints"
        """)
else:
    # Query interface
    query = st.text_input(
        "💬 Ask about the code",
        placeholder="Where is authentication handled?",
        help="Ask any question about the codebase in natural language"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        search_button = st.button("🔍 Search", use_container_width=True)
    with col2:
        if st.session_state.get("query_history"):
            if st.button("🧹 Clear Memory", use_container_width=True):
                st.session_state["query_history"] = []
                st.session_state["context_memory"] = []
                st.success("Memory cleared!")
                st.rerun()
    
    # Show memory status
    if st.session_state.get("query_history"):
        with st.expander(f"🧠 Code Memory Active ({len(st.session_state['query_history'])} queries)"):
            for i, prev_q in enumerate(st.session_state["query_history"], 1):
                st.caption(f"{i}. {prev_q}")
    
    if search_button and query:
        with st.spinner("Searching codebase..."):
            # Build context-aware query (Code Memory Mode)
            enhanced_query = query
            if st.session_state["context_memory"]:
                recent_context = " ".join(st.session_state["context_memory"][-2:])
                enhanced_query = f"{recent_context} {query}"
            
            # Retrieve relevant files
            results = st.session_state["rag"].query(enhanced_query)
            
            # Generate AI answer if API key is available
            answer, has_ai = st.session_state["rag"].generate_answer(query, results)
            
            # Update memory
            st.session_state["query_history"].append(query)
            context_files = [r['path'] for r in results]
            st.session_state["context_memory"].append(f"Files: {', '.join(context_files[:2])}")
            
            # Keep memory manageable
            if len(st.session_state["query_history"]) > 5:
                st.session_state["query_history"] = st.session_state["query_history"][-5:]
                st.session_state["context_memory"] = st.session_state["context_memory"][-5:]
            
            # Display AI answer if available
            if has_ai and answer:
                st.markdown("### 🤖 AI Answer")
                st.markdown(answer)
                st.divider()
            elif answer and not has_ai:
                # Show error if there was one
                st.warning(answer)
                st.divider()
            else:
                # No API key configured
                st.info("💡 **AI answers not available** - Add a [FREE Gemini API key](https://makersuite.google.com/app/apikey) to get intelligent explanations. For now, here are the relevant code files:")
                st.divider()
            
            # Display retrieved files
            st.markdown("### 📚 Retrieved Code Files")
            
            for idx, r in enumerate(results, 1):
                with st.expander(f"📄 {r['path']}", expanded=(idx == 1)):
                    st.code(r["compressed"], language="python")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Original Tokens", r['original_tokens'])
                    with col2:
                        st.metric("Compressed Tokens", r['compressed_tokens'])
                    with col3:
                        reduction = 100 - int(r['compressed_tokens']/r['original_tokens']*100)
                        st.metric("Reduction", f"{reduction}%")

# Footer
st.divider()
st.caption("Built with Streamlit • Sentence Transformers • FAISS • Gemini AI")
