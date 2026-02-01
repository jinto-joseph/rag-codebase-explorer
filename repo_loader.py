"""Repository loader module.

Scans a local GitHub repository and loads code files for processing.
Supports Python (.py), JavaScript (.js), and TypeScript (.ts) files.
"""

import os

def load_repo(path):
    """Load all code files from a repository directory.
    
    Recursively walks the directory tree and loads Python, JavaScript,
    and TypeScript files. Handles encoding errors gracefully.
    
    Args:
        path (str): Absolute path to the repository root directory.
        
    Returns:
        list[dict]: List of dictionaries with 'path' and 'code' keys.
                    Example: [{'path': '/repo/file.py', 'code': 'def ...'}]
                    
    Example:
        >>> files = load_repo('/path/to/repo')
        >>> print(f"Loaded {len(files)} files")
    """
    files = []
    for root, _, filenames in os.walk(path):
        for f in filenames:
            if f.endswith((".py", ".js", ".ts")):
                full = os.path.join(root, f)
                try:
                    with open(full, "r", encoding="utf-8") as file:
                        files.append({
                            "path": full,
                            "code": file.read()
                        })
                except Exception as e:
                    # Silently skip files with encoding issues
                    pass
    return files
