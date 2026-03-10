# PageIndex Testing Application

A comprehensive Streamlit-based UI application for testing PageIndex samples with local Ollama integration.

![PageIndex Banner](https://pageindex.ai/static/images/pageindex_banner.jpg)

## 🎯 Overview

This application provides an interactive interface to test three PageIndex samples:

1. **💬 Chat Quickstart**: Simple document Q&A using PageIndex Chat API
2. **🔍 Simple RAG**: Reasoning-based retrieval with tree search
3. **👁️ Vision RAG**: Vision-based document analysis without OCR

All samples are adapted to use **local Ollama** with the **granite3-dense** model instead of OpenAI.

## ✨ Features

- ✅ Interactive Streamlit UI
- ✅ Local LLM integration via Ollama
- ✅ Three comprehensive demo modes
- ✅ Document upload and processing
- ✅ Real-time streaming responses
- ✅ Query history tracking
- ✅ Sample documents included

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
3. **PageIndex API Key** - Get from [dash.pageindex.ai](https://dash.pageindex.ai/api-keys)

### Installation

1. **Clone or download this repository**

2. **Run the launch script**:
   ```bash
   ./scripts/launch.sh
   ```

   This will:
   - Create a virtual environment
   - Install dependencies
   - Start the application

3. **Configure your API key**:
   - Copy `.env.example` to `.env`
   - Add your PageIndex API key

4. **Pull required Ollama models**:
   ```bash
   ollama pull granite3-dense:8b
   ollama pull llava  # For Vision RAG
   ```

5. **Access the application**:
   - Open your browser at `http://localhost:8501`

## 📖 Usage

### Starting the Application

```bash
./scripts/launch.sh
```

### Stopping the Application

```bash
./scripts/stop.sh
```

### Pushing to GitHub

```bash
./scripts/push_to_github.sh
```

This script:
- Creates/updates `.gitignore` to exclude `_*` folders
- Prompts for commit message
- Shows files to be committed
- Pushes to GitHub safely

## 📁 Project Structure

```
PageIndex-Test/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── modules/                   # Application modules
│   ├── ollama_client.py      # Ollama integration
│   ├── chat_quickstart.py    # Chat demo
│   ├── simple_rag.py         # Simple RAG demo
│   └── vision_rag.py         # Vision RAG demo
├── scripts/                   # Utility scripts
│   ├── launch.sh             # Start application
│   ├── stop.sh               # Stop application
│   └── push_to_github.sh     # Git push helper
├── Docs/                      # Documentation
│   ├── README.md             # Full documentation
│   ├── API_REFERENCE.md      # API documentation
│   └── TROUBLESHOOTING.md    # Common issues
├── input/                     # Sample documents
└── _sources/                  # Source notebooks (excluded from git)
```

## 🎓 Demos

### 1. Chat Quickstart

Simple document Q&A:
- Upload a PDF document
- Wait for processing
- Ask questions about the document
- Get streaming responses

### 2. Simple RAG

Reasoning-based retrieval:
- Upload a document
- Get PageIndex tree structure
- Perform reasoning-based tree search
- Generate answers from retrieved context

### 3. Vision RAG

Vision-based analysis:
- Upload a document
- Extract page images automatically
- Perform vision-based retrieval
- Answer questions using visual context

## 📚 Documentation

- **[Full Documentation](Docs/README.md)** - Complete guide
- **[API Reference](Docs/API_REFERENCE.md)** - API documentation
- **[Troubleshooting](Docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🔧 Configuration

Edit `.env` file:

```env
# PageIndex API Configuration
PAGEINDEX_API_KEY=your_pageindex_api_key_here

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3-dense:8b

# Application Configuration
APP_PORT=8501
```

## 🐛 Troubleshooting

### Cannot connect to Ollama

```bash
# Start Ollama
ollama serve
```

### Model not found

```bash
# Pull the model
ollama pull granite3-dense:8b
```

### Port already in use

```bash
# Stop existing instances
./scripts/stop.sh
```

For more issues, see [TROUBLESHOOTING.md](Docs/TROUBLESHOOTING.md)

## 📦 Dependencies

- `pageindex` - PageIndex SDK
- `streamlit` - Web UI framework
- `requests` - HTTP client
- `PyMuPDF` - PDF processing
- `python-dotenv` - Environment management
- `openai` - OpenAI-compatible interface

## 🔗 Links

- [PageIndex Homepage](https://vectify.ai)
- [PageIndex Dashboard](https://dash.pageindex.ai)
- [PageIndex API Docs](https://docs.pageindex.ai/quickstart)
- [PageIndex GitHub](https://github.com/VectifyAI/PageIndex)
- [Ollama](https://ollama.ai)

## 📄 License

This project is provided as-is for testing and educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

- **PageIndex**: [Discord](https://discord.com/invite/VuXuf29EUj)
- **Issues**: Open an issue on GitHub
- **Ollama**: [GitHub Issues](https://github.com/ollama/ollama/issues)

---

© 2025 PageIndex Testing Application