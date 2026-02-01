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
    
    Current implementation: keeps first 20 and last 20 lines for files
    with more than 40 lines. Future versions will integrate ScaleDown API
    for semantic-aware compression.
    
    Args:
        text (str): The code text to compress.
        
    Returns:
        str: Compressed version of the text.
        
    Example:
        >>> code = "\n".join([f"line {i}" for i in range(100)])
        >>> compressed = compress(code)
        >>> print(len(compressed.split("\n")))  # 41 lines (20+1+20)
    
    Note:
        This is a placeholder. Real ScaleDown API integration will
        preserve function signatures, class definitions, and key logic
        while removing boilerplate and less important code.
    """
    lines = text.split("\n")
    if len(lines) > 40:
        # Simple truncation: keep start and end
        text = "\n".join(lines[:20] + ["..."] + lines[-20:])
    return text
