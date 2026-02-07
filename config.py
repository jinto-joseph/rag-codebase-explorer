"""Configuration management for API keys and settings.

Handles API key loading from environment variables.
Gemini AI is OPTIONAL - app works without it!
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_gemini_api_key():
    """Get Gemini API key from environment or return None.
    
    Priority:
    1. Environment variable GEMINI_API_KEY (for Streamlit Cloud)
    2. Streamlit secrets (for deployment)
    3. None (app still works, just shows code without AI answers)
    
    Returns:
        str or None: Gemini API key if configured, None otherwise
        
    To get a FREE API key:
        1. Go to https://makersuite.google.com/app/apikey
        2. Click "Create API key"
        3. Copy and set as GEMINI_API_KEY environment variable
    """
    # Check environment variable first
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Check Streamlit secrets if available
    if api_key is None:
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except:
            pass
    
    return api_key

# Default settings
DEFAULT_CLONE_DIR = "temp_repos"
MAX_FILES_TO_PROCESS = 100  # Limit for large repos
SUPPORTED_EXTENSIONS = (".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".h")
