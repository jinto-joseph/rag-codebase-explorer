"""Test script to verify RAG Codebase Explorer setup.

Run this to check if all components are working correctly.
"""

import sys

def test_imports():
    """Test that all required packages are installed."""
    print("Testing imports...")
    try:
        import streamlit
        print("✅ Streamlit")
        import sentence_transformers
        print("✅ Sentence Transformers")
        import faiss
        print("✅ FAISS")
        import tiktoken
        print("✅ Tiktoken")
        from google import genai
        print("✅ Google GenAI SDK")
        import git
        print("✅ GitPython")
        import numpy
        print("✅ NumPy")
        try:
            import tree_sitter
            print("✅ tree-sitter (optional)")
            import tree_sitter_languages
            print("✅ tree-sitter-languages (optional)")
        except ImportError:
            print("⚠️ tree-sitter packages not installed (optional); fallback parser will be used.")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration and API key."""
    print("\nTesting configuration...")
    try:
        from config import get_gemini_api_key
        api_key = get_gemini_api_key()
        if api_key and len(api_key) > 0:
            print(f"✅ API key configured (length: {len(api_key)})")
            return True
        else:
            print("❌ API key not found")
            return False
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_components():
    """Test core components."""
    print("\nTesting core components...")
    try:
        from embedder import embed
        from compressor import compress, count_tokens
        from rag import CodeRAG
        
        # Test embedder
        test_text = "def hello(): print('world')"
        embedding = embed(test_text)
        print(f"✅ Embedder (dimension: {len(embedding)})")
        
        # Test compressor
        compressed = compress(test_text)
        tokens = count_tokens(test_text)
        print(f"✅ Compressor (tokens: {tokens})")
        
        # Test RAG
        rag = CodeRAG()
        print("✅ RAG initialization")
        
        return True
    except Exception as e:
        print(f"❌ Component error: {e}")
        return False

def test_repo_loader():
    """Test repository loader."""
    print("\nTesting repository loader...")
    try:
        from repo_loader import is_github_url
        
        # Test URL detection
        assert is_github_url("https://github.com/user/repo") == True
        assert is_github_url("/local/path") == False
        print("✅ GitHub URL detection")
        
        return True
    except Exception as e:
        print(f"❌ Repo loader error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("RAG CODEBASE EXPLORER - SETUP VERIFICATION")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Core Components", test_components()))
    results.append(("Repository Loader", test_repo_loader()))
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Load a GitHub repo URL")
        print("  3. Ask questions about the code!")
    else:
        print("⚠️ Some tests failed. Please install missing packages:")
        print("  pip install -r requirements.txt")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
