"""Free offline embeddings using Hugging Face sentence-transformers.

No API key required. Works completely offline after initial model download.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model (downloads once, then cached locally)
# This is FREE and works offline!
print("Loading embedding model (first time takes ~30 seconds to download)...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small, fast, free model
print("Model loaded! Ready to embed.")

def embed(text):
    """Generate embeddings using free Hugging Face model.
    
    No API key needed. Runs locally on your computer.
    
    Args:
        text (str): The text to embed.
        
    Returns:
        np.array: 384-dimensional embedding vector.
        
    Example:
        >>> v = embed("test code")
        >>> print(len(v))  # 384
    """
    try:
        # Generate embedding
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding
    except Exception as e:
        raise RuntimeError(f"Embedding failed: {e}")
