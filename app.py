"""
PageIndex Testing Application
A Streamlit UI for testing PageIndex samples with local Ollama
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.chat_quickstart import ChatQuickstartDemo
from modules.simple_rag import SimpleRAGDemo
from modules.vision_rag import VisionRAGDemo

# Page configuration
st.set_page_config(
    page_title="PageIndex Testing Application",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .demo-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

def check_configuration():
    """Check if required configuration is present"""
    api_key = os.getenv("PAGEINDEX_API_KEY")
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "granite3-dense:8b")
    
    issues = []
    if not api_key or api_key == "your_pageindex_api_key_here":
        issues.append("⚠️ PageIndex API key not configured")
    
    return {
        "api_key": api_key,
        "ollama_url": ollama_url,
        "ollama_model": ollama_model,
        "issues": issues
    }

def main():
    # Header
    st.markdown('<div class="main-header">📚 PageIndex Testing Application</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Test PageIndex samples with local Ollama integration</div>', unsafe_allow_html=True)
    
    # Check configuration
    config = check_configuration()
    
    # Sidebar
    with st.sidebar:
        st.image("https://pageindex.ai/static/images/pageindex_banner.jpg", use_container_width=True)
        st.markdown("---")
        
        st.subheader("⚙️ Configuration")
        
        if config["issues"]:
            for issue in config["issues"]:
                st.warning(issue)
            st.info("💡 Copy `.env.example` to `.env` and configure your API key")
        else:
            st.success("✅ Configuration loaded")
        
        st.markdown("---")
        st.subheader("🤖 Ollama Model Selection")
        
        # Get available models
        from modules.ollama_client import OllamaClient
        ollama_client = OllamaClient(config['ollama_url'], config['ollama_model'])
        
        if ollama_client.check_connection():
            available_models = ollama_client.list_models()
            
            if available_models:
                # Model selector
                selected_model = st.selectbox(
                    "Select Model:",
                    available_models,
                    index=available_models.index(config['ollama_model']) if config['ollama_model'] in available_models else 0,
                    help="Choose from your installed Ollama models"
                )
                
                # Update session state with selected model
                st.session_state['selected_model'] = selected_model
                
                # Show model info
                st.info(f"🎯 Using: {selected_model}")
                
                # Detect vision models
                vision_keywords = ['vision', 'llava', 'bakllava', 'qwen', 'minicpm']
                is_vision = any(keyword in selected_model.lower() for keyword in vision_keywords)
                
                if is_vision:
                    st.success("👁️ Vision-capable model detected")
                else:
                    st.warning("⚠️ Text-only model (Vision RAG may not work)")
            else:
                st.error("No models found. Run: `ollama pull <model>`")
        else:
            st.error("Cannot connect to Ollama")
        
        st.markdown("---")
        st.subheader("📊 System Info")
        st.text(f"Ollama URL: {config['ollama_url']}")
        
        st.markdown("---")
        st.subheader("📖 About")
        st.markdown("""
        This application demonstrates three PageIndex samples:
        
        1. **Chat Quickstart**: Simple document Q&A
        2. **Simple RAG**: Reasoning-based retrieval
        3. **Vision RAG**: Vision-based document analysis
        
        All samples use local Ollama with granite3-dense model instead of OpenAI.
        """)
        
        st.markdown("---")
        st.markdown("🔗 [PageIndex Docs](https://docs.pageindex.ai)")
        st.markdown("🔗 [GitHub Repo](https://github.com/VectifyAI/PageIndex)")
    
    # Main content
    tab1, tab2, tab3 = st.tabs([
        "💬 Chat Quickstart",
        "🔍 Simple RAG",
        "👁️ Vision RAG"
    ])
    
    with tab1:
        st.markdown("### 💬 Chat Quickstart Demo")
        st.markdown("""
        This demo shows how to:
        - Upload a document to PageIndex
        - Check processing status
        - Ask questions about the document
        """)
        
        if config["issues"]:
            st.error("⚠️ Please configure your API key in `.env` file to use this demo")
        else:
            selected_model = st.session_state.get('selected_model', config["ollama_model"])
            demo1 = ChatQuickstartDemo(config["api_key"], config["ollama_url"], selected_model)
            demo1.render()
    
    with tab2:
        st.markdown("### 🔍 Simple RAG Demo")
        st.markdown("""
        This demo demonstrates:
        - Building a PageIndex tree structure
        - Reasoning-based retrieval with tree search
        - Answer generation from retrieved context
        """)
        
        if config["issues"]:
            st.error("⚠️ Please configure your API key in `.env` file to use this demo")
        else:
            selected_model = st.session_state.get('selected_model', config["ollama_model"])
            demo2 = SimpleRAGDemo(config["api_key"], config["ollama_url"], selected_model)
            demo2.render()
    
    with tab3:
        st.markdown("### 👁️ Vision RAG Demo")
        st.markdown("""
        This demo showcases:
        - Vision-based document analysis
        - PDF page image extraction
        - Visual context reasoning without OCR
        """)
        
        if config["issues"]:
            st.error("⚠️ Please configure your API key in `.env` file to use this demo")
        else:
            selected_model = st.session_state.get('selected_model', config["ollama_model"])
            
            # Check if model is vision-capable
            vision_keywords = ['vision', 'llava', 'bakllava', 'qwen', 'minicpm']
            is_vision = any(keyword in selected_model.lower() for keyword in vision_keywords)
            
            if not is_vision:
                st.warning(f"⚠️ Model '{selected_model}' may not support vision. Consider using: llava, qwen-vl, or llama3.2-vision")
            
            demo3 = VisionRAGDemo(config["api_key"], config["ollama_url"], selected_model)
            demo3.render()

if __name__ == "__main__":
    main()

# Made with Bob
