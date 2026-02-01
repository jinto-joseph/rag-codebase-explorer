import os
import openai
import numpy as np

# Prefer using an environment variable for the API key.
# Set OPENAI_API_KEY in your environment instead of hardcoding keys.
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    openai.api_key = api_key
else:
    openai.api_key = None

def embed(text):
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY not set. Export it in your environment.")
    try:
        res = openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
    except Exception as e:
        raise RuntimeError(f"Embedding API call failed: {e}")

    try:
        return np.array(res.data[0].embedding)
    except Exception as e:
        raise RuntimeError(f"Unexpected embedding response shape: {e}")
