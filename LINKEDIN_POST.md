🧠 Built a RAG-based Code Navigator for large GitHub repos — fully local & free

Ever felt lost in a huge codebase?

I built a tool that lets you ask natural-language questions about a repository and get clear answers with file references, even for repos with 1000+ files.

🔍 What it does:

• Finds where logic like auth or DB usage lives

• Works offline (no paid APIs)

• Fast (~150ms responses)

• 🧠 Code Memory Mode: Remembers your previous queries for smarter follow-ups

The key ideas: RAG + prompt compression + conversation memory

Using ScaleDown-style compression, files shrink by 65–84% while keeping meaning (e.g. 393 → 138 tokens).

🛠 Built with:

Python, Streamlit, Sentence-Transformers, FAISS

🔗 Code & docs:  https://lnkd.in/g5tc2R5M

#RAG #DeveloperTools #BuildInPublic #AIEngineering #Python #OpenSource #GenAI #HPE #IntelUnnati