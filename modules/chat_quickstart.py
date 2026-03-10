"""
Chat Quickstart Demo Module
Based on pageIndex_chat_quickstart.ipynb
"""

import streamlit as st
import os
import time
from pathlib import Path
from pageindex import PageIndexClient


class ChatQuickstartDemo:
    """Demo for PageIndex Chat Quickstart"""
    
    def __init__(self, api_key: str, ollama_url: str, ollama_model: str):
        """
        Initialize Chat Quickstart Demo
        
        Args:
            api_key: PageIndex API key
            ollama_url: Ollama base URL
            ollama_model: Ollama model name
        """
        self.api_key = api_key
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.pi_client = PageIndexClient(api_key=api_key)
    
    def render(self):
        """Render the demo UI"""
        st.markdown("---")
        
        # File upload section
        st.subheader("📄 Step 1: Upload Document")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type=['pdf'],
                help="Upload a PDF document to analyze"
            )
        
        with col2:
            use_sample = st.checkbox("Use sample document", value=False)
            if use_sample:
                st.info("Using NVIDIA 10Q report sample")
        
        # Document submission
        if st.button("📤 Submit Document", type="primary", disabled=not (uploaded_file or use_sample)):
            with st.spinner("Uploading document to PageIndex..."):
                try:
                    if use_sample:
                        # Use sample document from input folder
                        sample_path = Path("input/13e6981b-95ed-4aac-a602-ebc5865d0590.pdf")
                        if sample_path.exists():
                            doc_id = self.pi_client.submit_document(str(sample_path))["doc_id"]
                        else:
                            st.error("Sample document not found in input folder")
                            return
                    else:
                        # Save uploaded file temporarily
                        temp_path = Path("temp") / uploaded_file.name
                        temp_path.parent.mkdir(exist_ok=True)
                        
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        doc_id = self.pi_client.submit_document(str(temp_path))["doc_id"]
                        
                        # Clean up temp file
                        temp_path.unlink()
                    
                    st.session_state['doc_id'] = doc_id
                    st.success(f"✅ Document submitted successfully! Document ID: `{doc_id}`")
                    
                except Exception as e:
                    st.error(f"❌ Error submitting document: {str(e)}")
        
        # Document status check
        if 'doc_id' in st.session_state:
            st.markdown("---")
            st.subheader("📊 Step 2: Check Processing Status")
            
            doc_id = st.session_state['doc_id']
            st.info(f"Document ID: `{doc_id}`")
            
            if st.button("🔄 Check Status"):
                with st.spinner("Checking document status..."):
                    try:
                        doc_info = self.pi_client.get_document(doc_id)
                        
                        status = doc_info.get('status', 'unknown')
                        
                        if status == 'completed':
                            st.success(f"✅ Document ready! ({doc_info.get('pageNum', 'N/A')} pages)")
                            st.session_state['doc_ready'] = True
                            
                            # Display document info
                            with st.expander("📋 Document Details"):
                                st.json(doc_info)
                        
                        elif status == 'processing':
                            st.warning("⏳ Document is still processing. Please wait and check again.")
                            st.session_state['doc_ready'] = False
                        
                        elif status == 'failed':
                            st.error("❌ Document processing failed.")
                            st.session_state['doc_ready'] = False
                        
                        else:
                            st.info(f"Status: {status}")
                            st.session_state['doc_ready'] = False
                    
                    except Exception as e:
                        st.error(f"❌ Error checking status: {str(e)}")
        
        # Question answering
        if st.session_state.get('doc_ready', False):
            st.markdown("---")
            st.subheader("💬 Step 3: Ask Questions")
            
            # Sample questions
            st.markdown("**Sample Questions:**")
            sample_questions = [
                "What is the revenue? Also show me which page I can find it.",
                "What are the main highlights of this document?",
                "Summarize the key financial metrics."
            ]
            
            selected_sample = st.selectbox(
                "Choose a sample question or write your own:",
                ["Custom question"] + sample_questions
            )
            
            if selected_sample == "Custom question":
                query = st.text_area(
                    "Enter your question:",
                    height=100,
                    placeholder="Type your question here..."
                )
            else:
                query = st.text_area(
                    "Enter your question:",
                    value=selected_sample,
                    height=100
                )
            
            if st.button("🔍 Ask Question", type="primary", disabled=not query):
                with st.spinner("Getting answer from PageIndex..."):
                    try:
                        doc_id = st.session_state['doc_id']
                        
                        # Stream response
                        response_placeholder = st.empty()
                        full_response = ""
                        
                        for chunk in self.pi_client.chat_completions(
                            messages=[{"role": "user", "content": query}],
                            doc_id=doc_id,
                            stream=True
                        ):
                            full_response += chunk
                            response_placeholder.markdown(f"**Answer:**\n\n{full_response}▌")
                        
                        response_placeholder.markdown(f"**Answer:**\n\n{full_response}")
                        
                        # Store in session state
                        if 'qa_history' not in st.session_state:
                            st.session_state['qa_history'] = []
                        
                        st.session_state['qa_history'].append({
                            'question': query,
                            'answer': full_response
                        })
                    
                    except Exception as e:
                        st.error(f"❌ Error getting answer: {str(e)}")
            
            # Display Q&A history
            if 'qa_history' in st.session_state and st.session_state['qa_history']:
                st.markdown("---")
                st.subheader("📜 Q&A History")
                
                for i, qa in enumerate(reversed(st.session_state['qa_history'])):
                    with st.expander(f"Q{len(st.session_state['qa_history']) - i}: {qa['question'][:50]}..."):
                        st.markdown(f"**Question:** {qa['question']}")
                        st.markdown(f"**Answer:** {qa['answer']}")

# Made with Bob
