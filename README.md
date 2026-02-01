# 🧠 Code Documentation Navigator (ScaleDown RAG)

An AI-powered system that lets you **search, understand, and navigate large GitHub codebases** using **RAG + ScaleDown compression**.

Instead of reading thousands of lines of code, just ask:

> "Where is authentication handled?"  
> "Which files use the database?"  
> "Explain this function in simple terms"

and get intelligent answers with file references.

---

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

- Python  
- Tree-sitter  
- ScaleDown API  
- FAISS / Chroma  
- OpenAI embeddings  
- Streamlit UI  

---

## 📂 Demo Repositories

This system was tested on:
- Repo 1 (small)
- Repo 2 (medium)
- Repo 3 (large)

Screenshots and benchmarks are in `/docs`.

---

## 🌟 Unique Feature — Code Memory Mode

The system remembers previously asked questions and uses them to improve future retrieval.

Example:  
If you ask:
> "Where is login?"

Then later:
> "How is password validated?"

It will reuse the login context.

This is described as:
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

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "your-key-here"

# Linux/Mac
export OPENAI_API_KEY="your-key-here"
```

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Load a Repository
- Enter the path to a local GitHub repo
- Click "Load Repo"
- Ask questions about the code

---

## 📚 Documentation

- [Architecture](docs/architecture.md) - System design and RAG flow
- [Benchmarks](docs/benchmarks.md) - Performance metrics and compression stats
- [Screenshots](docs/Screenshots/README.md) - Demo queries and results

---

## 📌 Author

Built by **Jinto Joseph**  
B.Tech CSE | AI & RAG Explorer
