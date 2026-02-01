# 🧠 RAG Codebase Explorer  
*ScaleDown-powered AI for understanding large GitHub repositories*

RAG Codebase Explorer is an AI system that lets you **search, understand, and explore large codebases** using **Retrieval-Augmented Generation (RAG)** and **ScaleDown prompt compression**.

Instead of manually reading thousands of lines of code, just ask:

> “Where is authentication handled?”  
> “Which files talk to the database?”  
> “Explain this function in simple terms.”

And the system gives you intelligent, file-aware answers.

---

## 🚀 Why This Exists

Modern software projects are huge.  
Large Language Models fail when code exceeds context limits.

This project solves that using **ScaleDown compression**, allowing the AI to:
- Read very large files
- Preserve meaning
- Understand entire modules in one query

This makes real-world codebases finally usable with AI.

---

## 🧠 How It Works

GitHub Repository  
↓  
Tree-sitter Parser  
↓  
Function & Class Chunking  
↓  
ScaleDown Compression  
↓  
Embeddings  
↓  
Vector Database  
↓  
RAG Query Engine  
↓  
AI Answers with File References

---

## ✨ Features

- 🔍 Natural-language code search  
- 📄 Automatic documentation generation  
- 🧩 Dependency & usage analysis  
- 🔧 Refactoring suggestions  
- ⚡ Token-efficient ScaleDown compression  

---

## 📊 ScaleDown Impact

| Metric | Without Compression | With ScaleDown |
|-------|-------------------|---------------|
| Avg tokens per file | ~5000 | ~800 |
| Files per query | 1–2 | Entire module |
| Cost | High | 75% lower |
| Accuracy | Drops on big files | Preserved |

---

## 🛠 Tech Stack

- Python  
- Tree-sitter  
- ScaleDown API  
- OpenAI embeddings  
- FAISS / Chroma vector database  
- Streamlit UI  

---

## 📂 Tested On

This system was validated on:
- A small GitHub repo  
- A medium-sized repo  
- A large open-source project  

Screenshots, logs, and benchmarks are available in `/docs`.

---

## 🌟 Unique Feature — Code Memory Mode

The system remembers previous questions and retrieved files during a session.  
This allows **multi-turn reasoning across a large codebase**, enabling deeper understanding over time without reloading everything.

---

## 🎯 What Makes This Different

Unlike simple “code chatbots”, RAG Codebase Explorer:
- Understands **function-level structure**
- Uses **compressed context**
- Scales to **real-world codebases**

This makes it usable for professional software projects.

---

## 📌 Author

Built by **Jinto Joseph**  
B.Tech CSE | AI & RAG Explorer


