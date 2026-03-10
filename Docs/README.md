# PageIndex Testing Application

A comprehensive Streamlit-based UI application for testing PageIndex samples with local Ollama integration.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)

## 🎯 Overview

This application provides an interactive interface to test three PageIndex samples:

1. **Chat Quickstart**: Simple document Q&A using PageIndex Chat API
2. **Simple RAG**: Reasoning-based retrieval with tree search
3. **Vision RAG**: Vision-based document analysis without OCR

All samples are adapted to use local Ollama with the granite3-dense model instead of OpenAI.

## ✨ Features

- **Interactive UI**: Clean, intuitive Streamlit interface
- **Local LLM Integration**: Uses Ollama for all LLM operations
- **Three Demo Modes**: 
  - Chat Quickstart for simple Q&A
  - Simple RAG for reasoning-based retrieval
  - Vision RAG for visual document analysis
- **Document Management**: Upload and process PDF documents
- **Real-time Processing**: Stream responses and track processing status
- **History Tracking**: Keep track of all queries and responses
- **Sample Documents**: Pre-loaded sample documents for quick testing

## 📦 Prerequisites

### Required Software

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **Ollama**
   - Install from: https://ollama.ai
   - Start Ollama service:
     ```bash
     ollama serve
     ```

3. **Ollama Models**
   - Pull the granite3-dense model:
     ```bash
     ollama pull granite3-dense:8b
     ```
   - For Vision RAG, also pull a vision model:
     ```bash
     ollama pull llava
     ```

### PageIndex API Key

Get your API key from: https://dash.pageindex.ai/api-keys

## 🚀 Installation

### Quick Start

1. **Clone or download the repository**

2. **Run the launch script**:
   ```bash
   ./scripts/launch.sh
   ```

   This script will:
   - Create a virtual environment
   - Install all dependencies
   - Start the application

### Manual Installation

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# PageIndex API Configuration
PAGEINDEX_API_KEY=your_pageindex_api_key_here

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3-dense:8b

# Application Configuration
APP_PORT=8501
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `PAGEINDEX_API_KEY` | Your PageIndex API key | Required |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model to use for text generation | `granite3-dense:8b` |
| `APP_PORT` | Streamlit application port | `8501` |

## 📖 Usage

### Starting the Application

**Using the launch script** (recommended):
```bash
./scripts/launch.sh
```

**Manual start**:
```bash
source venv/bin/activate
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Stopping the Application

**Using the stop script**:
```bash
./scripts/stop.sh
```

**Manual stop**:
Press `Ctrl+C` in the terminal running the application

### Using the Demos

#### 1. Chat Quickstart Demo

1. Navigate to the "💬 Chat Quickstart" tab
2. Upload a PDF or use the sample document
3. Click "Submit Document"
4. Wait for processing to complete
5. Check document status
6. Ask questions about the document

#### 2. Simple RAG Demo

1. Navigate to the "🔍 Simple RAG" tab
2. Upload a PDF or use the sample document
3. Get the PageIndex tree structure
4. Enter a query for reasoning-based retrieval
5. Perform tree search to find relevant nodes
6. Generate an answer based on retrieved context

#### 3. Vision RAG Demo

1. Navigate to the "👁️ Vision RAG" tab
2. Upload a PDF or use the sample document
3. The system extracts page images automatically
4. Get the PageIndex tree structure
5. Enter a query about visual elements
6. Perform vision-based search
7. Generate an answer using visual context

### Sample Documents

The application includes sample documents in the `input/` folder:

- `13e6981b-95ed-4aac-a602-ebc5865d0590.pdf`: NVIDIA 10Q report
- `1706.03762v7.pdf`: "Attention Is All You Need" paper
- `2501.12948v2.pdf`: Research paper sample

## 🏗️ Architecture

### Project Structure

```
PageIndex-Test/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your configuration (not in git)
├── modules/                   # Application modules
│   ├── __init__.py
│   ├── ollama_client.py      # Ollama integration
│   ├── chat_quickstart.py    # Chat demo module
│   ├── simple_rag.py         # Simple RAG demo module
│   └── vision_rag.py         # Vision RAG demo module
├── scripts/                   # Utility scripts
│   ├── launch.sh             # Application launcher
│   ├── stop.sh               # Application stopper
│   └── push_to_github.sh     # Git push helper
├── Docs/                      # Documentation
│   ├── README.md             # This file
│   ├── API_REFERENCE.md      # API documentation
│   ├── ARCHITECTURE.md       # Architecture details
│   └── TROUBLESHOOTING.md    # Common issues and solutions
├── input/                     # Sample documents
└── _sources/                  # Source notebooks (excluded from git)
```

### Component Overview

#### Main Application (`app.py`)
- Streamlit UI setup
- Configuration management
- Tab-based navigation
- Demo orchestration

#### Ollama Client (`modules/ollama_client.py`)
- Ollama API integration
- OpenAI-compatible interface
- Vision model support
- Async operations

#### Demo Modules
- **Chat Quickstart**: Direct PageIndex Chat API usage
- **Simple RAG**: Tree-based reasoning retrieval
- **Vision RAG**: Visual context analysis

## 🔧 Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for detailed solutions.

### Common Issues

#### Cannot connect to Ollama
```
⚠️ Cannot connect to Ollama. Please ensure Ollama is running.
```

**Solution**: Start Ollama service
```bash
ollama serve
```

#### API Key not configured
```
⚠️ PageIndex API key not configured
```

**Solution**: Edit `.env` file with your API key

#### Model not found
```
Error: model 'granite3-dense:8b' not found
```

**Solution**: Pull the model
```bash
ollama pull granite3-dense:8b
```

#### Port already in use
```
Error: Port 8501 is already in use
```

**Solution**: Stop existing Streamlit instances
```bash
./scripts/stop.sh
```

## 📚 API Reference

See [API_REFERENCE.md](./API_REFERENCE.md) for detailed API documentation.

### PageIndex Client

```python
from pageindex import PageIndexClient

client = PageIndexClient(api_key="your_api_key")

# Submit document
doc_id = client.submit_document("path/to/document.pdf")["doc_id"]

# Check status
doc_info = client.get_document(doc_id)

# Get tree structure
tree = client.get_tree(doc_id, node_summary=True)["result"]

# Chat with document
for chunk in client.chat_completions(
    messages=[{"role": "user", "content": "Your question"}],
    doc_id=doc_id,
    stream=True
):
    print(chunk, end="", flush=True)
```

### Ollama Client

```python
from modules.ollama_client import OllamaClient

client = OllamaClient(
    base_url="http://localhost:11434",
    model="granite3-dense:8b"
)

# Generate text
response = client.generate("Your prompt here")

# Chat completion
response = await client.chat_completion(
    messages=[{"role": "user", "content": "Hello"}]
)

# Vision chat
response = client.chat_with_vision(
    prompt="Describe this image",
    image_paths=["path/to/image.jpg"]
)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is provided as-is for testing and educational purposes.

## 🔗 Links

- [PageIndex Homepage](https://vectify.ai)
- [PageIndex Dashboard](https://dash.pageindex.ai)
- [PageIndex API Docs](https://docs.pageindex.ai/quickstart)
- [PageIndex GitHub](https://github.com/VectifyAI/PageIndex)
- [Ollama](https://ollama.ai)

## 📧 Support

For issues related to:
- **PageIndex**: Visit [PageIndex Discord](https://discord.com/invite/VuXuf29EUj)
- **This Application**: Open an issue on GitHub
- **Ollama**: Visit [Ollama GitHub](https://github.com/ollama/ollama)

---

© 2025 PageIndex Testing Application