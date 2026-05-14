# PageIndex Testing Application (Local Edition): Project Context

This project is a Streamlit-based testing suite for PageIndex-style "Tree Search" RAG, refactored to run entirely locally using **Ollama** or **OMLX**.

## 🚀 Key Commands

- **Launch:** `./scripts/launch.sh`
- **Stop:** `./scripts/stop.sh`

## 📂 Project Structure

```
PageIndex-Test/
├── config.json                 # Settings (Ollama/OMLX URLs)
├── src/
│   └── pageindex_test/         # Application package
│       ├── main.py             # Entry point
│       ├── modules/            # Local Analysis logic
│       └── llm/                # LLM/VLM providers
└── input/                      # Sample documents
```

## 📝 Development Conventions

- **Multimodal by Default:** Every document is processed into a hierarchical tree containing both text and images.
- **Local Reasoning:** All RAG tasks are performed locally; no remote API keys are used.
- **Configuration:** Settings are managed in `config.json`.
