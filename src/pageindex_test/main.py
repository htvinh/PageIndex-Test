"""
PageIndex Testing Application (Local-Only Mode)
A Streamlit UI for testing PageIndex-style RAG with local LLMs (Ollama/OMLX)
"""

import json
import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to path for src package imports
sys.path.append(str(Path(__file__).parent.parent))

from pageindex_test.modules.doc_analysis import DocAnalysisDemo
from pageindex_test.modules.llm.ollama_llm import OllamaLLM
from pageindex_test.modules.llm.omlx_llm import OmlxLLM

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()

# Page configuration
st.set_page_config(
    page_title="Document Analysis and Question Answering Application",
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
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">📚 Document Analysis and Querying Application</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Local Tree Search RAG with Ollama & oMLX</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        #st.image("https://pageindex.ai/static/images/pageindex_banner.jpg", width="stretch")
        #st.markdown("---")
        
        st.subheader("⚙️ LLM Provider Selection")

        provider_type = st.radio(
            "Select LLM Provider",
            ["OMLX", "Ollama"],
            help="Choose the local LLM engine to use for reasoning and generation"
        )

        enable_vision = st.checkbox("Enable Vision Analysis", value=False, help="Include images in retrieval if enabled")
        st.session_state['enable_vision'] = enable_vision

        st.markdown("---")

        
        if provider_type == "Ollama":
            st.subheader("🤖 Ollama Configuration")
            ollama_url = config["ollama"]["url"]
            ollama_host = ollama_url.split("//")[-1].split(":")[0]
            ollama_port = int(ollama_url.split(":")[-1])
            
            from pageindex_test.modules.ollama_client import OllamaClient
            temp_client = OllamaClient(ollama_url)
            
            if temp_client.check_connection():
                available_models = config["ollama"]["models"]
                default_model = config["ollama"]["default_model"]
                
                selected_model = st.selectbox(
                    "Select Ollama Model:",
                    available_models,
                    index=available_models.index(default_model) if default_model in available_models else 0
                )
                
                llm = OllamaLLM(host=ollama_host, port=ollama_port, model=selected_model)
                st.success(f"✅ Connected to Ollama: {selected_model}")
            else:
                st.error("❌ Cannot connect to Ollama. Ensure 'ollama serve' is running.")
                llm = None
                
        else: # OMLX
            st.subheader("🤖 oMLX Configuration")
            omlx_url = config["omlx"]["url"]
            
            selected_model = st.selectbox(
                "Select OMLX Model:",
                config["omlx"]["models"],
                index=config["omlx"]["models"].index(config["omlx"]["default_model"])
            )
            
            st.text(f"URL: {omlx_url}")
            
            llm = OmlxLLM(base_url=omlx_url, model=selected_model)
            st.info("💡 Ensure your OMLX server is running.")

        st.markdown("---")
        st.subheader("📖 About Local Mode")
        st.markdown("""
        This version runs entirely locally:
        - Reasoning-based tree search.
        - Visual document analysis.
        
        No API key or remote connection is required.
        """)
    
    # Main content
    if llm:
        #st.markdown("### 📚 Document Analysis (Local)")
        #st.markdown("Unified reasoning over document text and visual context.")
        
        demo = DocAnalysisDemo(llm=llm)
        demo.render()
    else:
        st.warning("⚠️ Please configure and connect to an LLM provider in the sidebar to begin.")

if __name__ == "__main__":
    main()
