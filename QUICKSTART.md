# 🚀 Quick Start

## For Local Development

### 1. Clone and Setup
```bash
git clone https://github.com/jinto-joseph/rag-codebase-explorer.git
cd rag-codebase-explorer

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. (Optional) Add Gemini API Key
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```
📖 Get a free key: https://makersuite.google.com/app/apikey

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Use It!
- Load any GitHub repo URL or local path
- Ask questions about the code
- Get AI-powered answers (with API key) or code file results

---

## For Streamlit Cloud Deployment

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Deploy RAG Code Navigator"
git push
```

### 2. Deploy on Streamlit
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select this repository
4. Set main file: `app.py`
5. **Add Gemini API key in Secrets** (Settings → Secrets):
```toml
GEMINI_API_KEY = "your_api_key_here"
```
6. Click "Deploy" ✅

### 3. Use It!
- Load any GitHub repo URL (e.g., `https://github.com/streamlit/streamlit`)
- Ask questions about the code
- Get AI-powered answers!

---

## Important Notes

### ✅ What Works on Streamlit Cloud
- **GitHub URL input** - Clone and analyze any public repository
- **AI-powered answers** - Gemini API is already configured
- **No file uploads needed** - Perfect for cloud deployment

### ⚠️ What Doesn't Work on Streamlit Cloud
- **Local file paths** - Can't access your computer files on cloud
- **Private repositories** - Requires authentication (use public repos)

---

## Example Usage

**Step 1:** Load a repository
```
Input: https://github.com/streamlit/streamlit
Click: Load Repository
```

**Step 2:** Ask questions
```
"Where is the main Streamlit app class defined?"
"Which files handle user authentication?"
"Explain how caching works in this codebase"
```

**Step 3:** Get AI answers with code references!

---

## Tech Info

- **Model:** gemini-1.5-flash (fast, efficient)
- **Embeddings:** sentence-transformers (FREE, offline)
- **Vector DB:** FAISS
- **Config:** Uses `.env` file or environment variables

---

## Need Help?

- See [GET_API_KEY.md](GET_API_KEY.md) for API key setup
- Check [README.md](README.md) for project overview
- Open an issue if you encounter problems

**Your app is ready! 🎉**
