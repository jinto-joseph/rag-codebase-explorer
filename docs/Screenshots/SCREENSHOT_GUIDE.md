# 📸 Screenshot Guide - What to Capture

Add these **8 essential screenshots** to make your project look professional and demo-ready.

---

## 🎯 Required Screenshots (8 Total)

### 1. **01_main_interface.png**
**What to capture:**
- Clean view of the Streamlit app homepage
- "RAG Codebase Explorer" title visible
- Empty path input field
- "Load Repo" button visible

**Why:** Shows the starting point and clean UI

---

### 2. **02_loading_repo.png**
**What to capture:**
- Path entered in the input field (your test repo)
- Loading spinner or progress message
- "Files found: X" message

**Example path to use:**
- Windows: `C:\Users\YourName\Projects\test-repo`
- Show the system processing files

**Why:** Demonstrates the ingestion phase

---

### 3. **03_repo_loaded_success.png**
**What to capture:**
- Success message: "Loaded X files"
- The processed file list or summary
- Token statistics visible

**Why:** Shows successful repository loading

---

### 4. **04_query_authentication.png**
**What to capture:**
- Query input field with text: **"Where is authentication handled?"**
- The "Search" button
- Before clicking search

**Why:** Shows natural language query input

---

### 5. **05_search_results_auth.png**
**What to capture:**
- Query: "Where is authentication handled?"
- Top 3 results showing:
  - File paths (e.g., `auth.py`, `middleware/auth.py`)
  - Compressed code snippets
  - Token counts (Original → Compressed)

**Example result:**
```
### auth.py
def login(user, password):
    ...
Tokens: 5200 → 820
```

**Why:** Demonstrates accurate retrieval and compression

---

### 6. **06_query_database.png**
**What to capture:**
- Different query: **"Which files use the database?"**
- Search results showing database-related files
- Multiple relevant files returned

**Example files shown:**
- `models.py`
- `db.py`
- `database/connection.py`

**Why:** Shows versatility with different query types

---

### 7. **07_token_statistics.png**
**What to capture:**
- Close-up of token statistics
- Show multiple files with:
  - Original tokens: ~5000
  - Compressed tokens: ~800
  - Compression percentage: ~84%

**Highlight:**
- Create a text overlay or arrow pointing to the savings
- Show total tokens saved

**Why:** Proves the ScaleDown compression impact

---

### 8. **08_multiple_results.png**
**What to capture:**
- Complex query: **"Find all error handling functions"**
- All 3 results visible on screen
- Scroll to show file paths, code, and stats for each

**Why:** Shows full result set and UI completeness

---

## 🎨 Optional But Impressive Screenshots

### 9. **09_compression_comparison.png**
**Create a side-by-side:**
- Left: Full file code (500+ lines)
- Right: Compressed version (40 lines)
- Arrows showing "5200 tokens → 820 tokens"

**Tool:** Use screenshot + image editor or PowerPoint

**Why:** Visual proof of compression effectiveness

---

### 10. **10_architecture_diagram.png**
**What to capture:**
- Open [docs/architecture.md](docs/architecture.md)
- Screenshot the ASCII flowchart section
- Shows RAG pipeline visually

**Why:** Demonstrates system understanding

---

## 🛠️ How to Capture These

### Quick Workflow:

1. **Start the app:**
   ```powershell
   streamlit run app.py
   ```

2. **Prepare a test repository:**
   - Use your own code project (10-50 files)
   - OR clone a small open-source repo

3. **Capture systematically:**
   - Screenshot 1: Homepage
   - Enter path → Screenshot 2
   - Click Load → Screenshot 3
   - Enter query → Screenshot 4
   - View results → Screenshot 5
   - Repeat for 2-3 different queries → Screenshots 6-8

4. **Save to this folder:**
   ```
   docs/Screenshots/01_main_interface.png
   docs/Screenshots/02_loading_repo.png
   ...etc
   ```

---

## 💡 Pro Tips for Great Screenshots

### Preparation
- ✅ Use **light theme** in VS Code/browser for clarity
- ✅ **Close unnecessary tabs/windows**
- ✅ **Maximize the Streamlit window** (full screen)
- ✅ Use **Ctrl + Mouse Wheel** to zoom if text is small

### Capture Quality
- ✅ Use **Windows Snipping Tool** (`Win + Shift + S`)
- ✅ Capture **entire app window** (including URL bar)
- ✅ **No personal info** visible (file paths with your name are OK)
- ✅ Save as **PNG** (better quality than JPG)

### Presentation
- ✅ Add **arrows or highlights** using Paint/PowerPoint if needed
- ✅ Keep **aspect ratio consistent** across screenshots
- ✅ File size: **< 500KB each** (compress if needed)

---

## 📋 Quick Checklist

Before you're done, verify you have:

- [ ] Screenshot showing the main UI
- [ ] Screenshot showing loading process
- [ ] Screenshot showing success message
- [ ] At least **3 different queries** with results
- [ ] Token statistics clearly visible
- [ ] File paths visible in results
- [ ] Compressed code snippets shown
- [ ] All files saved with clear names

---

## 🎯 Example Queries to Test

Use these proven queries for best results:

**Code Location Queries:**
- ✅ "Where is authentication handled?"
- ✅ "Which files use the database?"
- ✅ "Find all API routes"
- ✅ "Where is error handling?"

**Structure Queries:**
- ✅ "Show me the User class"
- ✅ "Find all models"
- ✅ "Which files import requests?"

**Documentation Queries:**
- ✅ "How does login work?"
- ✅ "Explain the database connection"
- ✅ "What does utils.py do?"

---

## 📊 What Good Screenshots Should Show

### For Judges/Reviewers:
1. **It works** (successful loading + queries)
2. **It's accurate** (relevant files returned)
3. **It's efficient** (token compression visible)
4. **It's usable** (clean UI, clear results)

### For LinkedIn/Portfolio:
1. Professional UI
2. Real queries with real results
3. Clear value proposition (compression stats)
4. Working system (not just mockups)

---

## 🚀 After Capturing Screenshots

1. **Add to README:**
   ```markdown
   ## 📸 Demo
   
   ![Main Interface](docs/Screenshots/01_main_interface.png)
   ![Search Results](docs/Screenshots/05_search_results_auth.png)
   ![Token Stats](docs/Screenshots/07_token_statistics.png)
   ```

2. **Use in presentations**
3. **Share on LinkedIn** (attach 1-2 best ones)
4. **Add to project documentation**

---

**Once you have these 8 screenshots, your project will look production-ready! 🎉**
