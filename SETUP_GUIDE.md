# 🚀 Quick Start Guide

Complete setup instructions for the Code Documentation Navigator.

---

## 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **No API keys required!** (Uses FREE local embeddings)

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/[YOUR_USERNAME]/rag-codebase-explorer.git
cd rag-codebase-explorer
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** First run will download the FREE embedding model (~23MB). After that, it works completely offline!

---

## 🎯 Usage

### Run the Application
```bash
streamlit run app.py
```

This will open the web interface at `http://localhost:8501`

### Load a Repository
1. Enter the **full path** to a local GitHub repository
   - Example (Windows): `C:\Users\YourName\Projects\my-repo`
   - Example (Mac/Linux): `/home/username/projects/my-repo`
2. Click **"Load Repo"**
3. Wait for processing (varies by repo size)

### Query the Codebase
1. Type a natural language question:
   - "Where is authentication handled?"
   - "Which files use the database?"
   - "Find the User class"
2. Click **"Search"**
3. View results with file paths, code, and token stats

---

## 🧪 Test with Sample Queries

**First run:** Downloads the FREE embedding model (~23MB, one-time only)  
**After that:** Works completely offline with zero costs!

Try these queries on your repository:

**Code Location:**
- "Where is the main function?"
- "Find error handling code"
- "Which files import requests?"

**Understanding:**
- "How does authentication work?"
- "Explain the database connection"
- "What does this module do?"

**Structure:**
- "List all API endpoints"
- "Find all class definitions"
- "Show configuration files"

---

## 📊 Understanding the Results

Each search returns **3 most relevant files** with:

- **Path:** Location of the file
- **Compressed Code:** ScaleDown-compressed version
- **Original Tokens:** Size before compression
- **Compressed Tokens:** Size after compression

**Token Reduction:** Typically 80-85% smaller!

---

## 🔧 Configuration (Advanced)

### Change Top-K Results
Edit [rag.py](rag.py#L30):
```python
# Change 3 to your desired number
D, I = self.index.search(np.array([qv]).astype("float32"), 5)
```

### Adjust Compression
Edit [compressor.py](compressor.py#L15):
```python
# Keep more or fewer lines
if len(lines) > 40:
    text = "\n".join(lines[:30] + ["..."] + lines[-30:])
```

### Use Different Embedding Model
Edit [embedder.py](embedder.py#L17):
```python
res = openai.embeddings.create(
    model="text-embedding-3-large",  # Larger, more accurate
    input=text
)
```

---

## 🐛 Troubleshooting

### "No embeddings created" Error
**Cause:** Missing or invalid API key

**Fix:**
```bash
# Verify API key is set
echo $env:OPENAI_API_KEY  # Windows
echo $OPENAI_API_KEY      # Mac/Linux

# Re-set the key
$env:OPENAI_API_KEY = "sk-your-key"
```

### "No files found" Error
**Cause:** Empty repository or wrong path

**Fix:**
- Verify the path is correct and absolute
- Ensure the repo contains `.py`, `.js`, or `.ts` files
- Check file permissions

### Slow Loading
**Cause:** Large repository or API rate limits

**Solutions:**
- Start with a small repo (10-20 files)
- OpenAI free tier has lower rate limits
- Upgrade to paid tier for faster processing

### ModuleNotFoundError
**Cause:** Missing dependencies

**Fix:**
```bash
pip install --upgrade -r requirements.txt
```

---

## 💰 Cost Estimation

### Embeddings Cost
- **Model:** text-embedding-3-small
- **Rate:** $0.0001 per 1K tokens
- **Average file:** 800 tokens (compressed) = $0.00008

### Example Costs
| Repo Size | Files | Total Cost |
|-----------|-------|-----------|
| Small | 20 | $0.002 |
| Medium | 100 | $0.008 |
| Large | 500 | $0.040 |

**Queries are nearly free** (~$0.000005 each)

---

## 📚 Next Steps

1. ✅ Load your first repository
2. ✅ Try the sample queries above
3. ✅ Capture screenshots for documentation
4. ✅ Share on LinkedIn using [LINKEDIN_POST.md](LINKEDIN_POST.md)
5. ✅ Explore the [architecture docs](docs/architecture.md)
6. ✅ Check out [benchmark results](docs/benchmarks.md)

---

## 🤝 Contributing

Want to improve this project?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Ideas welcome:
- Real ScaleDown API integration
- Tree-sitter AST parsing
- Persistent vector storage
- More compression strategies

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/[YOUR_USERNAME]/rag-codebase-explorer/issues)
- **Docs:** See `/docs` folder
- **Contact:** [Your Email/LinkedIn]

---

**Happy exploring! 🧠🚀**
