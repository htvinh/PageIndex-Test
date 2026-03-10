# Quick Start Guide

Get up and running with the PageIndex Testing Application in 5 minutes.

## 🚀 Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] Ollama installed and running
- [ ] PageIndex API key from [dash.pageindex.ai](https://dash.pageindex.ai/api-keys)

## 📦 Step 1: Setup

### 1.1 Navigate to Project Directory

```bash
cd PageIndex-Test
```

### 1.2 Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use your preferred editor
```

Update this line:
```env
PAGEINDEX_API_KEY=your_actual_api_key_here
```

### 1.3 Install Ollama Models

```bash
# Pull the main model (required)
ollama pull granite3-dense:8b

# Pull vision model (optional, for Vision RAG demo)
ollama pull llava
```

## 🎯 Step 2: Launch Application

### Option A: Using Launch Script (Recommended)

```bash
./scripts/launch.sh
```

This script will:
1. Create a virtual environment
2. Install all dependencies
3. Start the application
4. Open your browser automatically

### Option B: Manual Launch

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

## 🌐 Step 3: Access Application

The application will open automatically at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to this URL in your browser.

## 🎮 Step 4: Try Your First Demo

### Chat Quickstart Demo

1. Click on the **"💬 Chat Quickstart"** tab
2. Check the **"Use sample document"** checkbox
3. Click **"📤 Submit Document"**
4. Wait for processing (usually 30-60 seconds)
5. Click **"🔄 Check Status"** until status is "completed"
6. Enter a question like: "What is the revenue?"
7. Click **"🔍 Ask Question"**
8. Watch the streaming response!

## ✅ Verification

If everything is working, you should see:

- ✅ Green "Connected to Ollama" message
- ✅ Green "Configuration loaded" in sidebar
- ✅ Ability to upload documents
- ✅ Streaming responses to questions

## 🛑 Stopping the Application

### Using Stop Script

```bash
./scripts/stop.sh
```

### Manual Stop

Press `Ctrl+C` in the terminal where the application is running.

## 🔧 Troubleshooting

### Issue: Cannot connect to Ollama

**Solution:**
```bash
# Start Ollama in a new terminal
ollama serve
```

### Issue: API Key Error

**Solution:**
1. Verify your API key at [dash.pageindex.ai](https://dash.pageindex.ai/api-keys)
2. Ensure `.env` file exists and contains the correct key
3. Restart the application

### Issue: Model Not Found

**Solution:**
```bash
# Pull the required model
ollama pull granite3-dense:8b

# Verify it's installed
ollama list
```

### Issue: Port Already in Use

**Solution:**
```bash
# Stop existing instances
./scripts/stop.sh

# Or manually kill the process
lsof -ti:8501 | xargs kill -9
```

## 📚 Next Steps

Now that you're up and running:

1. **Try all three demos**:
   - 💬 Chat Quickstart
   - 🔍 Simple RAG
   - 👁️ Vision RAG

2. **Upload your own documents**:
   - Use the file uploader instead of sample documents
   - Try different types of PDFs

3. **Explore the documentation**:
   - [Full Documentation](README.md)
   - [API Reference](API_REFERENCE.md)
   - [Troubleshooting Guide](TROUBLESHOOTING.md)

## 🎓 Understanding the Demos

### Chat Quickstart
- **Purpose**: Simple Q&A with documents
- **Best for**: Quick questions about document content
- **Uses**: PageIndex Chat API directly

### Simple RAG
- **Purpose**: Reasoning-based retrieval
- **Best for**: Complex queries requiring context understanding
- **Uses**: PageIndex tree structure + Ollama for reasoning

### Vision RAG
- **Purpose**: Visual document analysis
- **Best for**: Questions about figures, diagrams, layouts
- **Uses**: PDF page images + vision-capable models

## 💡 Tips

1. **Start with sample documents** to verify everything works
2. **Use smaller documents** for faster processing during testing
3. **Check Ollama logs** if responses seem slow or incorrect
4. **Keep the terminal open** to see application logs
5. **Use the history feature** to track your queries

## 🆘 Getting Help

If you encounter issues:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review application logs in the terminal
3. Verify Ollama is running: `curl http://localhost:11434/api/tags`
4. Check PageIndex status: Visit [dash.pageindex.ai](https://dash.pageindex.ai)

## 🎉 Success!

You're now ready to explore PageIndex with local Ollama integration!

---

**Estimated Setup Time**: 5-10 minutes  
**Difficulty**: Beginner-friendly  
**Support**: See [README.md](../README.md) for support links