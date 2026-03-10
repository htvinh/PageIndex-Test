# Troubleshooting Guide

This guide covers common issues and their solutions for the PageIndex Testing Application.

## 📋 Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Ollama Issues](#ollama-issues)
- [PageIndex API Issues](#pageindex-api-issues)
- [Application Issues](#application-issues)
- [Performance Issues](#performance-issues)

## 🔧 Installation Issues

### Python Version Error

**Problem**: `Python 3.8+ required`

**Solution**:
```bash
# Check Python version
python3 --version

# Install Python 3.8+ if needed
# macOS (using Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11
```

### Pip Installation Fails

**Problem**: `pip: command not found`

**Solution**:
```bash
# Install pip
python3 -m ensurepip --upgrade

# Or use get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### Virtual Environment Creation Fails

**Problem**: `venv module not found`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install python3-venv

# macOS (should be included with Python)
python3 -m pip install virtualenv
```

### Dependency Installation Errors

**Problem**: `Failed building wheel for [package]`

**Solution**:
```bash
# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Install build dependencies (Ubuntu/Debian)
sudo apt install python3-dev build-essential

# macOS
xcode-select --install

# Retry installation
pip install -r requirements.txt
```

## ⚙️ Configuration Issues

### Missing .env File

**Problem**: `⚠️ Warning: .env file not found!`

**Solution**:
```bash
# Copy example file
cp .env.example .env

# Edit with your API key
nano .env  # or use your preferred editor
```

### Invalid API Key

**Problem**: `401 Unauthorized` or `Invalid API key`

**Solution**:
1. Get a valid API key from https://dash.pageindex.ai/api-keys
2. Update `.env` file:
   ```env
   PAGEINDEX_API_KEY=your_actual_api_key_here
   ```
3. Restart the application

### Environment Variables Not Loading

**Problem**: Configuration not being read

**Solution**:
```bash
# Ensure .env is in the project root
ls -la .env

# Check file permissions
chmod 644 .env

# Verify python-dotenv is installed
pip install python-dotenv

# Restart application
./scripts/stop.sh
./scripts/launch.sh
```

## 🤖 Ollama Issues

### Cannot Connect to Ollama

**Problem**: `⚠️ Cannot connect to Ollama. Please ensure Ollama is running.`

**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Or run in background (macOS/Linux)
nohup ollama serve > /dev/null 2>&1 &
```

### Ollama Not Installed

**Problem**: `ollama: command not found`

**Solution**:
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### Model Not Found

**Problem**: `Error: model 'granite3-dense:8b' not found`

**Solution**:
```bash
# Pull the required model
ollama pull granite3-dense:8b

# For Vision RAG, also pull a vision model
ollama pull llava

# List available models
ollama list
```

### Ollama Port Conflict

**Problem**: `Port 11434 already in use`

**Solution**:
```bash
# Find process using port
lsof -i :11434

# Kill the process
kill -9 [PID]

# Or use a different port
# Update .env:
OLLAMA_BASE_URL=http://localhost:11435

# Start Ollama on different port
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

### Slow Model Response

**Problem**: Model takes too long to respond

**Solution**:
1. **Use a smaller model**:
   ```bash
   ollama pull granite3-dense:2b
   ```
   Update `.env`:
   ```env
   OLLAMA_MODEL=granite3-dense:2b
   ```

2. **Increase timeout** in `modules/ollama_client.py`:
   ```python
   response = requests.post(url, json=payload, timeout=300)  # 5 minutes
   ```

3. **Check system resources**:
   ```bash
   # Monitor CPU/Memory
   top
   
   # Check GPU usage (if applicable)
   nvidia-smi
   ```

## 📡 PageIndex API Issues

### Document Upload Fails

**Problem**: `❌ Error submitting document`

**Solution**:
1. **Check file size**: PageIndex has file size limits
2. **Verify PDF format**: Ensure file is a valid PDF
3. **Check API quota**: You may have reached your API limit
4. **Network issues**: Check internet connection

### Document Processing Stuck

**Problem**: Document stays in "processing" status

**Solution**:
1. **Wait longer**: Large documents take time
2. **Check document status**:
   ```python
   doc_info = client.get_document(doc_id)
   print(doc_info)
   ```
3. **Resubmit if failed**: If status is "failed", resubmit
4. **Contact support**: If stuck for >30 minutes

### Rate Limit Exceeded

**Problem**: `429 Too Many Requests`

**Solution**:
1. **Wait before retrying**: Respect rate limits
2. **Upgrade plan**: Consider higher tier for more requests
3. **Implement retry logic**: Add exponential backoff

### Tree Structure Empty

**Problem**: `get_tree()` returns empty or incomplete tree

**Solution**:
1. **Check if retrieval ready**:
   ```python
   if client.is_retrieval_ready(doc_id):
       tree = client.get_tree(doc_id)
   ```
2. **Wait for processing**: Document must be fully processed
3. **Check document format**: Some PDFs may not parse correctly

## 🖥️ Application Issues

### Port Already in Use

**Problem**: `Error: Port 8501 is already in use`

**Solution**:
```bash
# Stop existing Streamlit instances
./scripts/stop.sh

# Or manually kill process
lsof -ti:8501 | xargs kill -9

# Use different port
streamlit run app.py --server.port 8502
```

### Application Won't Start

**Problem**: Application crashes on startup

**Solution**:
1. **Check logs**:
   ```bash
   streamlit run app.py 2>&1 | tee app.log
   ```

2. **Verify dependencies**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check Python version**:
   ```bash
   python3 --version  # Should be 3.8+
   ```

4. **Clear Streamlit cache**:
   ```bash
   rm -rf ~/.streamlit/cache
   ```

### Module Import Errors

**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep [module_name]
```

### Session State Issues

**Problem**: Session state not persisting or causing errors

**Solution**:
1. **Clear browser cache**: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
2. **Restart application**: Stop and start again
3. **Check Streamlit version**:
   ```bash
   pip install --upgrade streamlit
   ```

### File Upload Fails

**Problem**: Cannot upload PDF files

**Solution**:
1. **Check file size**: Streamlit has upload limits
2. **Verify file format**: Must be valid PDF
3. **Check permissions**: Ensure temp directory is writable
4. **Increase upload limit** in `.streamlit/config.toml`:
   ```toml
   [server]
   maxUploadSize = 200
   ```

## 🚀 Performance Issues

### Slow Application Response

**Problem**: UI is slow or unresponsive

**Solution**:
1. **Reduce concurrent operations**: Process one document at a time
2. **Clear session state**: Restart application
3. **Check system resources**:
   ```bash
   # Monitor resources
   htop  # or top
   ```
4. **Optimize Ollama**: Use smaller models or increase resources

### Memory Issues

**Problem**: `MemoryError` or application crashes

**Solution**:
1. **Use smaller documents**: Test with smaller PDFs first
2. **Increase system memory**: Close other applications
3. **Use smaller models**:
   ```bash
   ollama pull granite3-dense:2b
   ```
4. **Process in batches**: Don't load too many documents

### PDF Image Extraction Slow

**Problem**: Vision RAG image extraction takes too long

**Solution**:
1. **Reduce image quality** in `modules/vision_rag.py`:
   ```python
   mat = fitz.Matrix(1.5, 1.5)  # Lower from 2.0
   ```
2. **Process fewer pages**: Limit page range
3. **Use smaller PDFs**: Test with shorter documents

## 🔍 Debugging Tips

### Enable Debug Mode

Add to `.streamlit/config.toml`:
```toml
[logger]
level = "debug"

[runner]
fastReruns = false
```

### Check Logs

```bash
# Application logs
tail -f app.log

# Ollama logs
journalctl -u ollama -f  # Linux with systemd

# Streamlit logs
~/.streamlit/logs/
```

### Test Components Individually

```python
# Test Ollama connection
from modules.ollama_client import OllamaClient
client = OllamaClient()
print(client.check_connection())

# Test PageIndex connection
from pageindex import PageIndexClient
client = PageIndexClient(api_key="your_key")
print(client.list_models())
```

## 📞 Getting Help

If you're still experiencing issues:

1. **Check GitHub Issues**: Search for similar problems
2. **PageIndex Discord**: https://discord.com/invite/VuXuf29EUj
3. **Ollama GitHub**: https://github.com/ollama/ollama/issues
4. **Create an Issue**: Provide:
   - Error message
   - Steps to reproduce
   - System information
   - Logs

## 🔄 Reset Everything

If all else fails, start fresh:

```bash
# Stop application
./scripts/stop.sh

# Remove virtual environment
rm -rf venv

# Remove cache
rm -rf __pycache__ modules/__pycache__
rm -rf ~/.streamlit/cache

# Remove temporary files
rm -rf temp pdf_images

# Reinstall
./scripts/launch.sh
```

---

Still having issues? Open an issue on GitHub with detailed information about your problem.