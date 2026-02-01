"""Code compression module using ScaleDown principles.

Provides token counting and compression functions to reduce
code file sizes while preserving semantic meaning.
"""

import tiktoken

def count_tokens(text):
    """Count the number of tokens in text using OpenAI's tokenizer.
    
    Uses the cl100k_base encoding (GPT-4 tokenizer) to count tokens.
    Essential for cost estimation and context window management.
    
    Args:
        text (str): The text to tokenize and count.
        
    Returns:
        int: Number of tokens in the text.
        
    Example:
        >>> code = "def hello(): return 'world'"
        >>> tokens = count_tokens(code)
        >>> print(f"Tokens: {tokens}")
    """
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def compress(text):
    """Compress code text using simple truncation strategy.
    
    Simulates ScaleDown compression by removing middle sections of code
    while preserving beginning and end (where key logic usually is).
    
    Args:
        text (str): The code text to compress.
        
    Returns:
        str: Compressed version of the text.
        
    Example:
        >>> code = "\n".join([f"line {i}" for i in range(100)])
        >>> compressed = compress(code)
        >>> print(len(compressed.split("\n")))  # ~35 lines
    """
    lines = text.split("\n")
    
    # Compress if file has more than 15 lines (adjusted for smaller files)
    if len(lines) > 15:
        # Keep first 10 and last 10 lines, add "..." in middle
        keep_start = min(10, len(lines) // 3)
        keep_end = min(10, len(lines) // 3)
        text = "\n".join(lines[:keep_start] + ["# ... (compressed middle section) ..."] + lines[-keep_end:])
    
    return text
