# 🧠 System Architecture — RAG Codebase Explorer

This document explains how the RAG Codebase Explorer processes large codebases using Retrieval-Augmented Generation (RAG) and ScaleDown compression.

---

## 🔍 High-Level Flow

The system follows this pipeline:

GitHub Repository  
→ Tree-sitter Parser  
→ Function & Class Chunking  
→ ScaleDown Compression  
→ Embeddings  
→ Vector Database  
→ RAG Query Engine  
→ AI Answer with File References  

---

## 🧩 RAG Flow

1. Source code is loaded from a GitHub repository.
2. Tree-sitter parses files into structured components like:
   - functions
   - classes
   - modules
3. Each code unit is treated as a retrievable document.
4. User queries are converted into embeddings.
5. Relevant code chunks are retrieved from the vector database.
6. The LLM receives the retrieved context and produces a final answer.

This allows the system to answer questions about code without reading the entire repository at once.

---

## ⚡ Where ScaleDown Fits

ScaleDown is applied **before embeddings are created**.

Each function, class, or module is compressed using ScaleDown so that:
- Token count is reduced
- Semantic meaning is preserved
- Large files become usable inside LLM context windows

This allows the system to handle much larger codebases than normal RAG systems.

---

## 📉 Why Compression Matters

Without compression:
- Large files exceed LLM token limits
- Retrieval becomes expensive
- Important context is dropped

With ScaleDown:
- Full files fit into a single query
- Costs are reduced
- Retrieval accuracy improves
- Multi-file reasoning becomes possible

This makes real-world codebases AI-friendly.

---

## 🎯 Goal

The goal of this architecture is to make AI-assisted code navigation practical, scalable, and affordable.
