# 🚀 Deployment Guide

## Streamlit Cloud Deployment (Recommended)

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [streamlit.io](https://streamlit.io))
- Gemini API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Step-by-Step Instructions

#### 1. Push Your Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/rag-codebase-explorer.git
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `yourusername/rag-codebase-explorer`
4. Main file path: `app.py`
5. Click "Deploy"

#### 3. Configure API Key (Optional)

The app already includes your API key as a fallback, but for better security:

1. In your Streamlit Cloud dashboard, click on your app
2. Click "⚙️ Settings"
3. Go to "Secrets" section
4. Add your API key in TOML format:

```toml
GEMINI_API_KEY = "2tWXt6dZDZ1SYgd0RtNZi1U2I2JSIT0a2gAfiqJ7"
```

5. Click "Save"

#### 4. Test Your Deployment

1. Wait for the app to build (2-3 minutes)
2. Open your app URL: `https://yourusername-rag-codebase-explorer.streamlit.app`
3. Try loading a GitHub repository:
   - Example: `https://github.com/streamlit/streamlit`
4. Ask questions about the code!

---

## Local Development

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rag-codebase-explorer.git
cd rag-codebase-explorer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
streamlit run app.py
```

4. **Open in browser**
The app will automatically open at `http://localhost:8501`

---

## Usage Guide

### Loading a Repository

**Option 1: GitHub URL (Recommended for Deployment)**
1. Select "GitHub URL" in the sidebar
2. Enter a GitHub repository URL
   - Example: `https://github.com/streamlit/streamlit`
3. Click "🚀 Load Repository"
4. Wait for processing (may take 30-60 seconds)

**Option 2: Local Path (Development Only)**
1. Select "Local Path" in the sidebar
2. Enter the absolute path to a local repository
   - Windows: `C:\Users\YourName\projects\myrepo`
   - Mac/Linux: `/Users/yourname/projects/myrepo`
3. Click "🚀 Load Repository"

### Asking Questions

Once a repository is loaded:

1. **Type your question** in the text input
   - "Where is authentication handled?"
   - "Which files use the database?"
   - "Explain the main API routes"

2. **Click "🔍 Search"**

3. **Review results:**
   - AI-generated answer at the top
   - Retrieved code files below with compression stats

### Code Memory Mode

The app remembers your previous queries for context-aware conversations:

- Ask follow-up questions naturally
- Memory stores the last 5 queries
- Click "🧹 Clear Memory" to reset

---

## Troubleshooting

### "No supported code files found"
- Ensure the repository contains Python, JavaScript, TypeScript, Java, C++, or C files
- Check that the GitHub URL is correct and public

### "Error loading repository: Authentication failed"
- For private repos, the current version only supports public repositories
- Make the repository public or use a local path

### "Error generating answer: API key invalid"
- Verify your API key in `config.py` or Streamlit secrets
- Get a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### App is slow
- Large repositories (>100 files) may take 1-2 minutes to process
- The first run downloads the embedding model (~23MB)
- Subsequent runs are faster with cached models

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | No | Hardcoded fallback | Gemini API key for answer generation |

---

## Supported File Types

- Python (`.py`)
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`, `.tsx`)
- Java (`.java`)
- C++ (`.cpp`)
- C (`.c`, `.h`)

---

## Limits

- Maximum files processed: 100 (configurable in `config.py`)
- Maximum tokens per query: ~30,000 (Gemini Pro limit)
- GitHub repo size: Unlimited (uses shallow clone)

---

## Security Notes

### API Key Security

**Current Setup:**
- API key is included with fallback for ease of use
- For production, use environment variables

**Best Practices:**
1. Never commit `.env` files to GitHub
2. Use Streamlit Secrets for deployed apps
3. Rotate API keys regularly
4. Monitor API usage in Google Cloud Console

### Repository Cloning

- Only clone trusted repositories
- Cloned repos are temporary and deleted after processing
- No code is executed, only read and analyzed

---

## Performance Optimization

### For Large Repositories

1. **Increase file limit** in `config.py`:
```python
MAX_FILES_TO_PROCESS = 200  # Default: 100
```

2. **Use smaller repos** for testing
3. **Filter by file type** in `config.py`:
```python
SUPPORTED_EXTENSIONS = (".py",)  # Only Python files
```

---

## Cost Estimation

### Gemini API Usage
- FREE tier: 60 requests/minute
- Each query = 1 API call
- Typical usage: <$0.01 per session

### Streamlit Cloud
- FREE tier: 1 app, unlimited usage
- Sufficient for most use cases

---

## Next Steps

- ⭐ Star the repository on GitHub
- 📝 Report issues or request features
- 🔧 Customize for your specific codebase
- 📊 Share your deployment and feedback!

---

## Support

For issues or questions:
- Check the [README.md](README.md)
- Review the [architecture documentation](docs/architecture.md)
- Open a GitHub issue

Happy coding! 🚀
