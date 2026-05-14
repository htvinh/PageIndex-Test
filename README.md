# PageIndex Testing Application (Local Edition)

A professional-grade testing suite for PageIndex-style RAG, optimized for local operation with **Ollama** or **OMLX**.

## 🎯 Overview

This application provides an interactive interface for local document reasoning. It is designed to be fully private, requiring no remote API keys or cloud connections.

- **Unified Analysis:** Reasoning-based search across multiple documents using local LLM/VLM providers.
- **Multimodal Support:** Analyzes both document text and page images simultaneously.
- **Hierarchical Retrieval:** Uses tree-based traversal for accurate context retrieval.

## 🚀 Quick Start

1. **Configure:** Update `config.json` with your Ollama/OMLX settings.
2. **Launch:** Run `./scripts/launch.sh`.
3. **Analyze:** Upload PDFs, aggregate them into your workspace, and ask complex cross-document questions.

## 📁 Project Structure

```
PageIndex-Test/
├── config.json                 # Project configuration
├── src/
│   └── pageindex_test/         # Application package
│       ├── main.py             # Entry point
│       ├── modules/            # Local PI client & Analysis logic
│       └── llm/                # LLM/VLM providers
├── scripts/                    # Utility scripts
└── input/                      # Sample documents
```
