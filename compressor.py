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

def _trim_code_body(code, target_tokens):
    """Trim a code body while retaining both signature-side and return-side context."""
    lines = code.split("\n")
    if len(lines) <= 40:
        return code

    head = min(35, max(10, len(lines) // 4))
    tail = min(35, max(10, len(lines) // 4))
    trimmed = "\n".join(lines[:head] + ["# ... scaledown middle omitted ..."] + lines[-tail:])

    if count_tokens(trimmed) <= target_tokens:
        return trimmed

    # tighter fallback
    head = min(20, len(lines) // 3)
    tail = min(20, len(lines) // 3)
    return "\n".join(lines[:head] + ["# ... scaledown middle omitted ..."] + lines[-tail:])


def compress(text, imports=None, dependencies=None, surrounding=None, target_tokens=800):
    """ScaleDown-style compression preserving structural and dependency context.

    Args:
        text (str): Core symbol code (function/class/module body).
        imports (list[str] | None): Related import statements.
        dependencies (list[str] | None): Related symbol references.
        surrounding (list[str] | None): Nearby function/class names.
        target_tokens (int): Approximate token budget per chunk.

    Returns:
        str: Context-preserving compressed chunk.
    """
    imports = imports or []
    dependencies = dependencies or []
    surrounding = surrounding or []

    core = _trim_code_body(text, max(300, target_tokens - 250))
    sections = []

    if imports:
        sections.append("## Imports\n" + "\n".join(imports[:15]))
    if dependencies:
        sections.append("## Dependencies\n" + ", ".join(dependencies[:15]))
    if surrounding:
        sections.append("## Surrounding Symbols\n" + ", ".join(surrounding[:6]))
    sections.append("## Core Code\n" + core)

    compressed = "\n\n".join(sections)

    if count_tokens(compressed) <= target_tokens:
        return compressed

    # Secondary pass: reduce context lists before shrinking core further.
    reduced_imports = imports[:8]
    reduced_dependencies = dependencies[:8]
    reduced_surrounding = surrounding[:4]
    core = _trim_code_body(text, max(220, target_tokens - 180))
    sections = []
    if reduced_imports:
        sections.append("## Imports\n" + "\n".join(reduced_imports))
    if reduced_dependencies:
        sections.append("## Dependencies\n" + ", ".join(reduced_dependencies))
    if reduced_surrounding:
        sections.append("## Surrounding Symbols\n" + ", ".join(reduced_surrounding))
    sections.append("## Core Code\n" + core)
    return "\n\n".join(sections)
