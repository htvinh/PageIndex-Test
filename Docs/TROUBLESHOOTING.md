# Troubleshooting Guide (Local Mode)

## 🤖 Connection Issues
- **Ollama:** Ensure `ollama serve` is running. Check `config.json` for correct URL.
- **OMLX:** Ensure OMLX server is running at the configured URL.

## 🖥️ Application Issues
- **Launch Errors:** Run `./scripts/stop.sh` to clear existing processes.
- **Processing Errors:** If document processing fails, check logs: `tail -f streamlit.log`.

## 🔄 Reset Workspace
```bash
./scripts/stop.sh
rm -rf venv _local_storage temp
./scripts/launch.sh
```
