"""RAG (Retrieval-Augmented Generation) engine for code search.

Provides vector-based semantic search over compressed code files
using FAISS for efficient similarity matching.
"""

import faiss
import numpy as np
from embedder import embed

class CodeRAG:
    """Vector database and retrieval system for code navigation.
    
    Uses FAISS to index compressed code files and retrieve the most
    semantically similar files for a given natural language query.
    
    Attributes:
        texts (list): Stored file metadata (path, code, tokens).
        index (faiss.IndexFlatL2): FAISS vector index for similarity search.
    
    Example:
        >>> rag = CodeRAG()
        >>> rag.add([{'path': 'file.py', 'compressed': 'def ...'}])
        >>> results = rag.query("where is authentication?")
        >>> print(results[0]['path'])
    """
    def __init__(self):
        self.texts = []
        self.index = None

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
