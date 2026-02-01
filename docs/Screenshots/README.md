# 📸 Screenshots & Demo Queries

This folder contains visual demonstrations of the Code Documentation Navigator in action.

---

## 🎯 What to Include Here

### 1. **UI Screenshots**
Capture these key screens:
- Main interface (path input + load button)
- Loading progress/status
- Query interface
- Search results with file paths
- Token statistics display

### 2. **Query Examples**
Document these demo queries with screenshots:

**Basic Code Location:**
- "Where is authentication handled?"
- "Which files use the database?"
- "Find all API routes"

**Function/Class Search:**
- "Show me the User class"
- "Where is login validation?"
- "Find error handling functions"

**Dependency Analysis:**
- "Which files import requests?"
- "What modules use numpy?"
- "Find all database models"

**Documentation Queries:**
- "Explain the authentication flow"
- "How does payment processing work?"
- "What does this module do?"

### 3. **Performance Metrics**
Screenshot showing:
- Original vs compressed token counts
- Load time for different repo sizes
- Query response times
- Cost savings

### 4. **Compression Demo**
Side-by-side comparison:
- Full file (5000 tokens)
- Compressed version (800 tokens)
- Highlight preserved semantic content

---

## 📝 Screenshot Naming Convention

Use clear, descriptive names:
```
01_main_interface.png
02_loading_repo.png
03_query_authentication.png
04_search_results.png
05_token_statistics.png
06_compression_demo.png
07_multi_file_search.png
08_performance_metrics.png
```

---

## 🚀 How to Capture Screenshots

### Windows
1. Press `Win + Shift + S` for Snipping Tool
2. Select area to capture
3. Save to this folder

### Mac
1. Press `Cmd + Shift + 4`
2. Select area to capture
3. Save to this folder

### Linux
1. Use `gnome-screenshot` or `flameshot`
2. Select area and save

---

## 💡 Tips for Great Screenshots

1. **Clean UI:** Close unnecessary windows
2. **Readable Text:** Use zoom if needed
3. **Highlight Key Areas:** Use arrows/boxes to emphasize important parts
4. **Consistent Size:** Try to keep similar dimensions
5. **Good Lighting:** Use light VS Code themes for clarity

---

## 📊 Example Query Results to Capture

### Query: "Where is authentication handled?"
**Expected Results:**
- `auth.py` (login functions)
- `middleware/auth.py` (token validation)
- `models/user.py` (User model)

**Metrics to show:**
- Original tokens: 15,200
- Compressed tokens: 2,400
- Search time: 580ms

---

### Query: "Which files use the database?"
**Expected Results:**
- `models/*.py` (database models)
- `db.py` (connection setup)
- `migrations/*.py` (schema changes)

**Metrics to show:**
- Files found: 12
- Total tokens: 8,500 → 1,400
- Compression: 84%

---

## 🎬 Video Demo (Optional)

Consider recording a short video walkthrough:
1. Load a repository
2. Ask 3-4 queries
3. Show results and token stats
4. Highlight compression benefits

Upload to YouTube/Loom and link in main README.

---

## 📌 Next Steps

1. Run the app: `streamlit run app.py`
2. Load a test repository
3. Execute demo queries
4. Capture screenshots
5. Add them to this folder
6. Update main README with screenshot links

---

## 🔗 Linking Screenshots in Documentation

In README or docs, reference like this:

```markdown
![Main Interface](docs/Screenshots/01_main_interface.png)
![Query Results](docs/Screenshots/04_search_results.png)
```

---

**Happy documenting! 📸🚀**
