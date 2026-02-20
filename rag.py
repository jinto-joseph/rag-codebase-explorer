"""RAG (Retrieval-Augmented Generation) engine for code search.

Provides vector-based semantic search over compressed code files
using FAISS for efficient similarity matching and Gemini AI for
intelligent code understanding.
"""

import faiss
import numpy as np
from embedder import embed
from config import get_gemini_api_key
from google import genai

class CodeRAG:
    """Vector database and retrieval system for code navigation.
    
    Uses FAISS to index compressed code files and retrieve the most
    semantically similar files for a given natural language query.
    Integrates with Gemini AI to generate intelligent answers.
    
    Attributes:
        texts (list): Stored file metadata (path, code, tokens).
        index (faiss.IndexFlatL2): FAISS vector index for similarity search.
        gemini_model: Configured Gemini AI model for answer generation.
    
    Example:
        >>> rag = CodeRAG()
        >>> rag.add([{'path': 'file.py', 'compressed': 'def ...'}])
        >>> results = rag.query("where is authentication?")
        >>> print(results[0]['path'])
    """
    def __init__(self, api_key=None):
        self.texts = []
        self.index = None
        self.default_model = "gemini-2.0-flash"
        
        # Initialize Gemini AI (optional)
        self.gemini_model = None
        self.api_key_status = "not_configured"
        
        try:
            api_key = api_key or get_gemini_api_key()
            if api_key and len(api_key) > 20:
                self.gemini_model = genai.Client(api_key=api_key)
                self.api_key_status = "configured"
            else:
                self.api_key_status = "missing"
        except Exception as e:
            self.api_key_status = f"error: {str(e)}"

    def add(self, texts):
        """Add compressed code files to the vector database.
        
        Embeds each compressed file and builds a FAISS index for fast
        similarity search. Tracks failures to help with debugging.
        
        Args:
            texts (list[dict]): List of file dictionaries with keys:
                - 'compressed': The compressed code text
                - 'path': File path (for reference)
                - 'original_tokens': Token count before compression
                - 'compressed_tokens': Token count after compression
                
        Raises:
            ValueError: If no embeddings were successfully created.
                       Error message includes failure details.
        
        Example:
            >>> processed = [{'compressed': 'def f(): ...', 'path': 'a.py'}]
            >>> rag.add(processed)
        """
        self.texts = []
        vectors = []
        failures = []

        for t in texts:
            try:
                v = embed(t["compressed"])
                vectors.append(v)
                self.texts.append(t)
            except:
                # capture which file failed and why to help debugging
                try:
                    # include path if available
                    failures.append((t.get("path"), "embed failed"))
                except Exception:
                    failures.append((None, "embed failed"))

        if len(vectors) == 0:
            raise ValueError(f"No embeddings created. Check API key or repo files. Failures: {failures}")

        dim = len(vectors[0])
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(vectors).astype("float32"))

    def query(self, q):
        """Search for code files semantically similar to the query.
        
        Embeds the natural language query and finds the top-3 most
        similar code files using L2 distance in vector space.
        
        Args:
            q (str): Natural language query (e.g., "where is login?")
            
        Returns:
            list[dict]: Top-3 matching files with metadata:
                - 'path': File path
                - 'compressed': Compressed code content
                - 'original_tokens': Original token count
                - 'compressed_tokens': Compressed token count
                
        Example:
            >>> results = rag.query("authentication functions")
            >>> for r in results:
            ...     print(f"{r['path']}: {r['compressed_tokens']} tokens")
        """
        qv = embed(q)
        # Request up to 5 results, but handle repos with fewer chunks
        k = min(5, len(self.texts))
        D, I = self.index.search(np.array([qv]).astype("float32"), k)
        
        # Remove duplicates (FAISS may return same index multiple times)
        seen = set()
        results = []
        for i in I[0]:
            if i not in seen:
                seen.add(i)
                results.append(self.texts[i])
        return results
    
    def _build_usage_context(self):
        """Provide built-in project usage context for general help questions."""
        return (
            "Project quick usage guide:\n"
            "1. Install dependencies with: pip install -r requirements.txt\n"
            "2. Start app with: streamlit run app.py\n"
            "3. In sidebar, choose GitHub URL or Local Path.\n"
            "4. Load repository and ask code questions.\n"
            "5. For cloud deployment, prefer GitHub URL input.\n"
        )

    def _call_gemini(self, prompt):
        """Call Gemini and normalize error handling."""
        try:
            response = self.gemini_model.models.generate_content(
                model=self.default_model,
                contents=prompt,
            )
            return response.text, True
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg:
                return None, False
            if "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
                return "QUOTA_EXHAUSTED", False
            return f"⚠️ Error: {error_msg}", False

    def _mode_instruction(self, mode):
        if mode == "documentation":
            return (
                "Generate concise auto-documentation. Include purpose, inputs, outputs, and "
                "example usage for the most relevant symbols."
            )
        if mode == "dependencies":
            return (
                "Perform dependency analysis. Describe imports, symbol dependencies, and "
                "cross-symbol relationships in plain language."
            )
        if mode == "refactor":
            return (
                "Provide refactoring suggestions. Identify complexity hotspots, duplicated "
                "patterns, and give safe, practical improvements."
            )
        return (
            "Explain implementation clearly. Focus on where logic lives and how key symbols work."
        )

    def generate_answer(self, query, context_files, mode="explain"):
        """Generate an intelligent answer using Gemini AI based on retrieved code context.
        
        Takes the user's question and relevant code files to generate a comprehensive
        answer explaining where and how the functionality is implemented.
        
        Args:
            query (str): User's natural language question about the codebase.
            context_files (list[dict]): Retrieved code files with 'path' and 'compressed' keys.
            
        Returns:
            tuple: (answer_text, has_ai_answer) - AI answer and boolean indicating if AI was used
            
        Example:
            >>> results = rag.query("where is authentication?")
            >>> answer, has_ai = rag.generate_answer("where is authentication?", results)
            >>> print(answer)
        """
        if not self.gemini_model:
            return None, False
        
        # Build context from retrieved chunks
        context = "Here are the relevant code chunks:\n\n"
        for i, file in enumerate(context_files, 1):
            symbol = file.get("symbol", "module")
            chunk_type = file.get("chunk_type", "chunk")
            deps = ", ".join(file.get("dependencies", [])[:8]) or "none"
            context += (
                f"Chunk {i}: {file['path']}::{symbol} ({chunk_type})\n"
                f"Dependencies: {deps}\n"
                f"```\n{file['compressed']}\n```\n\n"
            )
        context += self._build_usage_context()
        
        # Create prompt for Gemini
        prompt = f"""You are a code intelligence assistant for large repositories.

User Question: {query}
Mode: {mode}

{context}

Provide a clear, concise answer that:
1. Directly answers the question
2. References specific file names and symbols
3. Highlights key functions/classes/modules involved
4. Follows this mode-specific instruction: {self._mode_instruction(mode)}

Answer:"""
        
        return self._call_gemini(prompt)

    def generate_general_answer(self, query):
        """Answer general project questions (e.g. setup/run/deploy) without repo context."""
        if not self.gemini_model:
            return None, False

        prompt = f"""You are a helpful assistant for this Streamlit project.

User Question: {query}

{self._build_usage_context()}

Answer with practical steps. If the question asks "how to run", include exact commands.
"""
        return self._call_gemini(prompt)

    def generate_local_documentation(self, context_files):
        """Generate a non-LLM documentation fallback from retrieved chunks."""
        lines = ["### 📘 Auto Documentation (Local Fallback)"]
        for item in context_files[:5]:
            path = item.get("path", "unknown")
            symbol = item.get("symbol", "module")
            chunk_type = item.get("chunk_type", "chunk")
            deps = item.get("dependencies", [])
            lines.append(f"- **{path} :: {symbol}** ({chunk_type})")
            if deps:
                lines.append(f"  - Dependencies: {', '.join(deps[:8])}")
            lines.append(f"  - Purpose: likely implements `{symbol}` behavior in `{path}`.")
            lines.append("  - Inputs/Outputs: inspect the code chunk below for exact signature and returns.")
        return "\n".join(lines)

    def generate_local_mode_answer(self, query, context_files, mode="explain"):
        """Generate local fallback answer for all analysis modes."""
        if mode == "documentation":
            return self.generate_local_documentation(context_files)

        top = context_files[:5]
        if mode == "dependencies":
            lines = ["### 🔗 Dependency Analysis (Local Fallback)"]
            for item in top:
                deps = item.get("dependencies", [])
                dep_text = ", ".join(deps[:10]) if deps else "No explicit local symbol dependencies detected."
                lines.append(f"- `{item.get('path')}::{item.get('symbol', 'module')}` → {dep_text}")
            return "\n".join(lines)

        if mode == "refactor":
            lines = ["### 🛠 Refactoring Suggestions (Local Fallback)"]
            lines.append("- Break very large modules into smaller focused files/classes.")
            lines.append("- Add clearer function-level docstrings for top retrieved symbols.")
            lines.append("- Reduce cross-module coupling for symbols with many dependencies.")
            for item in top[:3]:
                lines.append(f"- Candidate file: `{item.get('path')}` symbol `{item.get('symbol', 'module')}`.")
            return "\n".join(lines)

        lines = ["### 🧠 Explanation (Local Fallback)"]
        lines.append(f"Question: {query}")
        lines.append("Most relevant code locations:")
        for item in top:
            lines.append(
                f"- `{item.get('path')}::{item.get('symbol', 'module')}` "
                f"({item.get('chunk_type', 'chunk')})"
            )
        lines.append("Use the chunks below to inspect implementation details.")
        return "\n".join(lines)
