"""Repository loader module.

Scans a local GitHub repository or clones from a GitHub URL
and loads code files for processing.
Supports multiple programming languages.
"""

import os
import shutil
import tempfile
from urllib.parse import urlparse
from config import DEFAULT_CLONE_DIR, SUPPORTED_EXTENSIONS, MAX_FILES_TO_PROCESS

def is_github_url(path):
    """Check if the provided path is a GitHub URL.
    
    Args:
        path (str): Path or URL to check.
        
    Returns:
        bool: True if it's a GitHub URL, False otherwise.
    """
    return path.startswith("https://github.com") or path.startswith("http://github.com")

def clone_github_repo(url, target_dir=None):
    """Clone a GitHub repository to a temporary directory.
    
    Args:
        url (str): GitHub repository URL.
        target_dir (str, optional): Target directory. If None, uses temp directory.
        
    Returns:
        str: Path to the cloned repository.
        
    Raises:
        Exception: If cloning fails.
    """
    try:
        from git import Repo
        
        if target_dir is None:
            # Create unique temp directory with timestamp to avoid conflicts
            import time
            repo_name = os.path.basename(urlparse(url).path).replace(".git", "")
            timestamp = str(int(time.time()))[-6:]  # Last 6 digits of timestamp
            target_dir = os.path.join(DEFAULT_CLONE_DIR, f"{repo_name}_{timestamp}")
        
        # Try to remove existing directory if it exists (with retry logic for Windows)
        if os.path.exists(target_dir):
            try:
                shutil.rmtree(target_dir, onerror=_handle_remove_readonly)
            except Exception as e:
                # If removal fails, use a different directory name
                import random
                target_dir = f"{target_dir}_{random.randint(1000, 9999)}"
        
        os.makedirs(target_dir, exist_ok=True)
        
        # Clone the repository
        Repo.clone_from(url, target_dir, depth=1)  # Shallow clone for speed
        return target_dir
    except ImportError:
        raise ImportError("gitpython is required for cloning. Install it with: pip install gitpython")
    except Exception as e:
        raise Exception(f"Failed to clone repository: {str(e)}")

def _handle_remove_readonly(func, path, exc_info):
    """Error handler for Windows readonly file removal."""
    import stat
    if not os.access(path, os.W_OK):
        # Change the file to be writable and try again
        os.chmod(path, stat.S_IWUSR | stat.S_IREAD)
        func(path)
    else:
        raise

def load_repo(path):
    """Load all code files from a repository directory or GitHub URL.
    
    Supports both local paths and GitHub URLs. If a GitHub URL is provided,
    it will be cloned first. Recursively walks the directory tree and loads
    supported code files. Handles encoding errors gracefully.
    
    Args:
        path (str): Absolute path to repository root OR GitHub URL.
        
    Returns:
        tuple: (list[dict], str) - List of dictionaries with 'path' and 'code' keys,
               and the actual directory path used.
               Example: ([{'path': '/repo/file.py', 'code': 'def ...'}], '/repo')
                    
    Example:
        >>> files, repo_path = load_repo('https://github.com/user/repo')
        >>> print(f"Loaded {len(files)} files from {repo_path}")
    """
    # Handle GitHub URLs
    if is_github_url(path):
        actual_path = clone_github_repo(path)
    else:
        actual_path = path
    
    files = []
    file_count = 0
    
    for root, _, filenames in os.walk(actual_path):
        # Skip common directories that don't contain source code
        if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env']):
            continue
            
        for f in filenames:
            if file_count >= MAX_FILES_TO_PROCESS:
                break
                
            if f.endswith(SUPPORTED_EXTENSIONS):
                full = os.path.join(root, f)
                try:
                    with open(full, "r", encoding="utf-8") as file:
                        # Get relative path for cleaner display
                        rel_path = os.path.relpath(full, actual_path)
                        files.append({
                            "path": rel_path,
                            "code": file.read()
                        })
                        file_count += 1
                except Exception as e:
                    # Silently skip files with encoding issues
                    pass
        
        if file_count >= MAX_FILES_TO_PROCESS:
            break
    
    return files, actual_path
