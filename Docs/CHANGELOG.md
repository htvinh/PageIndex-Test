# Changelog

All notable changes to the PageIndex Testing Application.

## [1.2.1] - 2026-03-10

### Fixed

#### Vision RAG Display Error
- **Empty Results Handling**: Fixed `StreamlitInvalidColumnSpecError` when no images are retrieved
  - Added check for empty retrieved images list before creating columns
  - Shows informative message when no pages are retrieved
  - Prevents application crash on empty search results

## [1.2.0] - 2026-03-10

### Added

#### Detached Mode Support
- **Launch Script Enhancement**: Added support for running the application in detached (background) mode
  - Use `./scripts/launch.sh --detached` or `./scripts/launch.sh -d` to run in background
  - Logs are saved to `streamlit.log` for monitoring
  - Process ID (PID) is displayed for easy management
  - Default foreground mode remains unchanged for backward compatibility

#### Dynamic Model Selection
- **Model Dropdown**: Added dynamic model selection in the UI
  - Automatically detects all installed Ollama models
  - Displays models in a user-friendly dropdown
  - Updates all demos to use the selected model
  - Persists selection across page interactions using session state

#### Vision Model Detection
- **Smart Model Validation**: Added automatic detection of vision-capable models
  - Detects vision models using keywords (llava, qwen, minicpm, bakllava, cogvlm, yi-vl, deepseek-vl, internvl, moondream)
  - Shows warning when text-only models are selected for Vision RAG
  - Helps users avoid common configuration errors

### Fixed

#### GitHub Push Script
- **Graceful Handling**: Fixed script to handle "nothing to commit" scenarios
  - No longer exits with error when working directory is clean
  - Provides clear instructions when no remote repository is configured
  - Improved error messages and user guidance

### Changed

#### Documentation Updates
- Updated `README.md` with detached mode instructions
- Updated `Docs/README.md` with comprehensive launch options
- Updated `Docs/QUICK_START.md` with stopping instructions for both modes
- Added log viewing instructions for detached mode

#### Configuration
- Updated `.gitignore` to exclude `streamlit.log`
- Maintained exclusion of `_*/` folders for source materials

## [1.1.0] - 2026-03-09

### Added
- Initial release with three PageIndex demos
- Streamlit-based UI with tab navigation
- Ollama integration for local LLM inference
- Comprehensive documentation suite
- Launch, stop, and GitHub push scripts

### Features
- **Chat Quickstart**: Simple document Q&A using PageIndex Chat API
- **Simple RAG**: Reasoning-based retrieval with tree search
- **Vision RAG**: Vision-based document analysis without OCR
- **Document Management**: Upload and process PDF documents
- **Real-time Processing**: Stream responses and track status
- **History Tracking**: Keep track of queries and responses

## [1.0.0] - 2026-03-08

### Initial Development
- Project structure setup
- Core module development
- Documentation creation
- Script development

---

## Version History

- **1.2.1** (Current): Bug fix for Vision RAG empty results
- **1.2.0**: Detached mode, dynamic model selection, vision detection
- **1.1.0**: Initial release with three demos
- **1.0.0**: Development phase

## Upgrade Notes

### From 1.2.0 to 1.2.1

Bug fix release - no breaking changes.

**Fixed Issues:**
- Vision RAG no longer crashes when no images are retrieved

### From 1.1.0 to 1.2.0

No breaking changes. All existing functionality remains compatible.

**New Features Available:**
1. Run in detached mode: `./scripts/launch.sh --detached`
2. Select any installed Ollama model from the UI dropdown
3. Automatic vision model detection and warnings

**Recommended Actions:**
1. Pull the latest changes
2. Review the updated documentation
3. Try the new model selection feature
4. Test detached mode if you need background operation

## Future Roadmap

### Planned Features
- [ ] Multi-document comparison
- [ ] Export conversation history
- [ ] Custom model configuration per demo
- [ ] Performance metrics dashboard
- [ ] Batch document processing
- [ ] API endpoint for programmatic access

### Under Consideration
- [ ] Docker containerization
- [ ] Cloud deployment guides
- [ ] Additional LLM provider support
- [ ] Advanced visualization tools
- [ ] Collaborative features

## Contributing

See the main README.md for contribution guidelines.

## Support

For issues or questions:
1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the [API Reference](API_REFERENCE.md)
3. Open an issue on GitHub