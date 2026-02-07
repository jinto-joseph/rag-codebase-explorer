"""FREE embedding module using Hugging Face sentence-transformers.

NO API KEY REQUIRED - Works completely offline!
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# Load a TINY FREE model (downloads once ~23MB, then cached)
print("Loading FREE embedding model (downloading ~23MB)...")
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Smallest, fastest
print("✅ Model ready! No API key needed.")

def embed(text):
    """Generate embeddings using free local model.
    
    Args:
        text (str): Text to embed.
        
    Returns:
        np.array: 384-dimensional embedding vector.
    """
    try:
        return model.encode(text, convert_to_numpy=True)
    except Exception as e:
        raise RuntimeError(f"Embedding failed: {e}")

