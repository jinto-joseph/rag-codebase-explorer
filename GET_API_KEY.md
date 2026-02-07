# 🔑 How to Get Your FREE Gemini API Key

The app works perfectly **without** an API key - you'll see retrieved code files. But if you want **AI-powered answers**, follow these simple steps:

## 📝 Get Your Free API Key (2 minutes)

### Step 1: Go to Google AI Studio
Visit: **https://makersuite.google.com/app/apikey**

### Step 2: Sign in
- Use your Google account
- Accept the terms of service

### Step 3: Create API Key
1. Click **"Create API key"** button
2. Select **"Create API key in new project"** (or choose existing project)
3. Click **"Create API key"**
4. **Copy the key** (it looks like: `AIzaSyB...`)

⚠️ **Save it somewhere safe!** You won't be able to see it again.

---

## 🔧 Add API Key to Your App

### Option A: For Local Development (Windows)

**Using PowerShell:**
```powershell
# Set environment variable for current session
$env:GEMINI_API_KEY = "YOUR_API_KEY_HERE"

# Run the app
streamlit run app.py
```

**Permanent (recommended):**
```powershell
# Add to your PowerShell profile
notepad $PROFILE

# Add this line:
$env:GEMINI_API_KEY = "YOUR_API_KEY_HERE"

# Save and restart PowerShell
```

### Option B: For Local Development (Mac/Linux)

```bash
# Set environment variable
export GEMINI_API_KEY="YOUR_API_KEY_HERE"

# Run the app
streamlit run app.py
```

**Permanent:**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export GEMINI_API_KEY="YOUR_API_KEY_HERE"' >> ~/.bashrc
source ~/.bashrc
```

### Option C: For Streamlit Cloud Deployment

1. Go to your app on [share.streamlit.io](https://share.streamlit.io)
2. Click **⚙️ Settings**
3. Click **Secrets** in the sidebar
4. Add this in TOML format:

```toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

5. Click **Save**
6. Your app will restart automatically with AI answers enabled! 🎉

---

## ✅ Verify It's Working

### In the App:
- If configured correctly: No info banner at the top
- If not configured: Blue banner saying "Add a Gemini API key for AI-powered answers"

### Test It:
1. Load a repository
2. Search for something (e.g., "main function")
3. You should see **"🤖 AI Answer"** section at the top
4. Below that: **"📚 Retrieved Code Files"**

---

## 🆓 Free Tier Limits

Google's Gemini API free tier includes:
- **60 requests per minute**
- **1,500 requests per day**
- **FREE forever** (as of Feb 2025)

This is more than enough for personal projects and learning!

---

## 🔒 Security Best Practices

### ✅ DO:
- Set API keys as environment variables
- Use Streamlit Secrets for deployed apps
- Keep your API key private

### ❌ DON'T:
- Commit API keys to GitHub
- Share your API key publicly
- Hardcode keys in source files

---

## 🐛 Troubleshooting

### "API key not valid" error
- Double-check you copied the entire key
- Make sure there are no extra spaces
- Verify the key in Google AI Studio is still active

### Info banner still showing
- Restart the Streamlit app after setting the environment variable
- Check the variable is set: `echo $env:GEMINI_API_KEY` (Windows) or `echo $GEMINI_API_KEY` (Mac/Linux)

### "Quota exceeded" error
- You've hit the free tier limit (60/min or 1500/day)
- Wait a few minutes and try again
- The app will still show code files even without AI answers

---

## 🚀 Quick Test

After setting your API key, run this in PowerShell:

```powershell
# Check if API key is set
$env:GEMINI_API_KEY

# Should print your API key
# If empty, set it:
$env:GEMINI_API_KEY = "YOUR_API_KEY_HERE"

# Run the app
streamlit run app.py
```

---

## 💡 Remember

**The app works great without an API key!** You'll still get:
- ✅ Code search and retrieval
- ✅ Token compression
- ✅ File references
- ✅ Code snippets

The API key just adds:
- 🤖 Natural language explanations
- 🤖 Intelligent summaries
- 🤖 Context-aware answers

Both modes are useful! 🎯
