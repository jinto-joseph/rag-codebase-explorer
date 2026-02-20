# 🧠 Code Documentation Navigator (ScaleDown RAG)

An AI-powered system that lets you **search, understand, and navigate large GitHub codebases** using **RAG + ScaleDown compression**.

Instead of reading thousands of lines of code, just ask:

> "Where is authentication handled?"  
> "Which files use the database?"  
> "Explain this function in simple terms"

and get intelligent answers with file references.

---

## 🆕 Recent Updates

- **Stricter Face Recognition Security:**
   - Thresholds tightened to prevent unauthorized recognition (0.18 similarity, 10/12 matches, outlier checks).
   - Fixes previous issue where unregistered users could be recognized as the owner.
- **Enhanced Registration & Recognition:**
   - Higher camera resolution (1280x720), more samples, and quality validation.
   - Visual feedback and metadata storage for registration.
   - Improved recognition thresholds, real-time memory logging, and session management.
   - Multi-level detection (CNN, HOG, DNN, Haar Cascade) and better error handling.
   - Optimized performance and confidence calculation.

See `temp_repos/_583824/STRICT_RECOGNITION_FIX.md` and `temp_repos/_583824/RECOGNITION_IMPROVEMENTS.md` for details.

## 🚀 Why This Exists

Modern codebases are massive.  
LLMs fail when context exceeds token limits.

This project uses **ScaleDown prompt compression** to:
- Shrink large code files
- Preserve semantic meaning
- Enable whole-file understanding in a single query

---

## 🧠 How It Works

```
GitHub Repo
↓
Tree-sitter Parser
↓
Function/Class Chunking
↓
ScaleDown Compression
↓
Embeddings
↓
Vector Database
↓
RAG Query Engine
↓
AI Answers
```

---

## ✨ Key Features

- 🔍 Natural language code search  
- 📄 Auto documentation generator  
- 🧩 Dependency & usage tracking  
- 🔧 Refactoring suggestions  
- ⚡ Token-efficient ScaleDown compression  

---

## 📊 ScaleDown Impact

| Metric | Without Compression | With ScaleDown |
|-------|-------------------|---------------|
| Avg tokens per file | ~5000 | ~800 |
| Max file size | Limited | Whole-file |
| Cost | High | 75% lower |
| Accuracy | Drops on big files | Maintained |

---

## 🛠 Tech Stack

- **Python 3.8+**
- **Sentence-Transformers** (FREE embeddings - no API key!)
- **FAISS** vector database
- **Streamlit** UI
- **Google Gemini API** (gemini-1.5-flash) - Optional for AI answers
- **python-dotenv** for environment variable management
- Smart compression algorithms
- Tree-sitter (planned)

---

## 📸 Demo

### Main Interface
![Main Interface](docs/Screenshots/01_main_interface.png?raw=true)
*Clean, intuitive interface for code exploration*

### Loading Repository
![Loading Repository](docs/Screenshots/02_loading_repo.png?raw=true)
*Simple path input to load any local GitHub repository*

### Compression in Action
![Compression Working](docs/Screenshots/03_compression_working2.png?raw=true)
*Query: "login" - Found authentication code with 65% token compression (393 → 138 tokens)*

### Semantic Search Results
![Database Query](docs/Screenshots/04_query_database.png?raw=true)
*Query: "Which files handle database queries?" - Intelligent file retrieval with compression (583 → 336 tokens)*

---

## 📂 Demo Repositories

This system was tested on:

- Repo 1 (small)
- Repo 2 (medium)
- Repo 3 (large)

Screenshots and benchmarks are in `/docs`.

---

## 🌟 Unique Feature — Code Memory Mode

The system **remembers your previous queries** and automatically reuses context for smarter follow-up questions.

**How it works:**

1️⃣ **First query:** "Where is login handled?"
   - System finds `auth.py` and stores it in memory

2️⃣ **Follow-up query:** "How is password validated?"
   - System enhances your query with previous context: `"Previously searched: auth.py How is password validated?"`
   - Returns more accurate results by understanding the conversation flow

**Features:**
- 🧠 Tracks last 5 queries automatically
- 🔄 Combines current question with previous file context
- 📋 View query history in expandable panel
- 🗑️ Clear memory button to start fresh
- 💡 Visual indicator when memory is active

**Result:** Natural, multi-turn conversations with your codebase while keeping token usage minimal.

> **"Context-aware compressed memory for multi-turn code navigation."**

---

## 🎯 What Makes This Special

Unlike normal code chatbots, this system:
- Understands **function-level structure**
- Uses **compressed context**
- Handles **very large files**

This makes it practical for real-world developer use.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/jinto-joseph/rag-codebase-explorer.git
cd rag-codebase-explorer
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**No API keys needed!** Uses FREE offline embeddings.

### 4. (Optional) Add Gemini API Key for AI Answers

Create a `.env` file in the project root:
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

📖 See [GET_API_KEY.md](GET_API_KEY.md) for detailed instructions.

### 5. Run the App
```bash
streamlit run app.py
```

### 6. Load a Repository
- Enter a GitHub URL or local path
- Click "Load Repository"
- Ask questions about the code
- Get AI-powered answers (with API key) or view retrieved code files

---

## 📚 Documentation

- [Architecture](docs/architecture.md) - System design and RAG flow
- [Benchmarks](docs/benchmarks.md) - Performance metrics and compression stats
- [Screenshots](docs/Screenshots/) - Demo queries and results

---

## 📌 Author

Built by **Jinto Joseph**  
B.Tech CSE | AI & RAG Explorer
