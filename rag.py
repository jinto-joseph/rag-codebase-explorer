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
    def __init__(self):
        self.texts = []
        self.index = None
        
        # Initialize Gemini AI (optional)
        self.gemini_model = None
        self.api_key_status = "not_configured"
        
        try:
            api_key = get_gemini_api_key()
            if api_key and len(api_key) > 20:
                client = genai.Client(api_key=api_key)
                self.gemini_model = client
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
        # Request up to 3 results, but handle repos with fewer files
        k = min(3, len(self.texts))
        D, I = self.index.search(np.array([qv]).astype("float32"), k)
        
        # Remove duplicates (FAISS may return same index multiple times)
        seen = set()
        results = []
        for i in I[0]:
            if i not in seen:
                seen.add(i)
                results.append(self.texts[i])
        return results
    
    def generate_answer(self, query, context_files):
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
        
        # Build context from retrieved files
        context = "Here are the relevant code files:\n\n"
        for i, file in enumerate(context_files, 1):
            context += f"File {i}: {file['path']}\n```\n{file['compressed']}\n```\n\n"
        
        # Create prompt for Gemini
        prompt = f"""You are a code documentation expert. Analyze the following code files and answer the user's question.

User Question: {query}

{context}

Provide a clear, concise answer that:
1. Directly answers the question
2. References specific file names and locations
3. Explains the implementation briefly
4. Highlights key functions/classes involved

Answer:"""
        
        try:
            response = self.gemini_model.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return response.text, True
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg:
                return None, False
            return f"⚠️ Error: {error_msg}", False
