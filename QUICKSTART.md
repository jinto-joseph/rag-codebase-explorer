# 🚀 Quick Start (Streamlit Cloud)

## For Streamlit Cloud Deployment

Your API key is already configured! Just follow these steps:

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
5. Click "Deploy" ✅

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

## For Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then you can use **both** GitHub URLs and local paths.

---

## Need Help?

- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
- Check [README.md](README.md) for project overview
- Open an issue if you encounter problems

**Your app is ready to deploy! 🎉**
