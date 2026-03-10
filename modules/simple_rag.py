"""
Simple RAG Demo Module
Based on pageindex_RAG_simple.ipynb
"""

import streamlit as st
import json
import asyncio
from pathlib import Path
from pageindex import PageIndexClient
import pageindex.utils as utils
from .ollama_client import OllamaClient


class SimpleRAGDemo:
    """Demo for Simple Vectorless RAG with PageIndex"""
    
    def __init__(self, api_key: str, ollama_url: str, ollama_model: str):
        """
        Initialize Simple RAG Demo
        
        Args:
            api_key: PageIndex API key
            ollama_url: Ollama base URL
            ollama_model: Ollama model name
        """
        self.api_key = api_key
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.pi_client = PageIndexClient(api_key=api_key)
        self.ollama_client = OllamaClient(base_url=ollama_url, model=ollama_model)
    
    async def call_llm(self, prompt: str, temperature: float = 0.0) -> str:
        """Call LLM using Ollama"""
        return self.ollama_client.generate(prompt, temperature=temperature)
    
    def render(self):
        """Render the demo UI"""
        st.markdown("---")
        
        # Check Ollama connection
        if not self.ollama_client.check_connection():
            st.error("⚠️ Cannot connect to Ollama. Please ensure Ollama is running.")
            st.info(f"Expected URL: {self.ollama_url}")
            return
        
        st.success(f"✅ Connected to Ollama ({self.ollama_model})")
        
        # Step 1: Document Upload
        st.subheader("📄 Step 1: Upload Document")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type=['pdf'],
                key="simple_rag_upload",
                help="Upload a PDF document for RAG analysis"
            )
        
        with col2:
            use_sample = st.checkbox("Use sample document", value=False, key="simple_rag_sample")
            if use_sample:
                st.info("Using sample paper from input folder")
        
        if st.button("📤 Submit Document", type="primary", key="simple_rag_submit", disabled=not (uploaded_file or use_sample)):
            with st.spinner("Uploading document to PageIndex..."):
                try:
                    if use_sample:
                        # Use sample document from input folder
                        sample_path = Path("input/2501.12948v2.pdf")
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
                    
                    st.session_state['rag_doc_id'] = doc_id
                    st.success(f"✅ Document submitted! Document ID: `{doc_id}`")
                    
                except Exception as e:
                    st.error(f"❌ Error submitting document: {str(e)}")
        
        # Step 2: Get Tree Structure
        if 'rag_doc_id' in st.session_state:
            st.markdown("---")
            st.subheader("🌳 Step 2: Get PageIndex Tree Structure")
            
            doc_id = st.session_state['rag_doc_id']
            
            if st.button("🔄 Get Tree Structure", key="get_tree"):
                with st.spinner("Fetching tree structure..."):
                    try:
                        if self.pi_client.is_retrieval_ready(doc_id):
                            tree = self.pi_client.get_tree(doc_id, node_summary=True)['result']
                            st.session_state['rag_tree'] = tree
                            
                            st.success("✅ Tree structure retrieved!")
                            
                            # Display simplified tree
                            with st.expander("📋 View Tree Structure"):
                                tree_str = self._format_tree(tree)
                                st.code(tree_str, language="text")
                        else:
                            st.warning("⏳ Document is still processing. Please wait and try again.")
                    
                    except Exception as e:
                        st.error(f"❌ Error getting tree: {str(e)}")
        
        # Step 3: Reasoning-Based Retrieval
        if 'rag_tree' in st.session_state:
            st.markdown("---")
            st.subheader("🔍 Step 3: Reasoning-Based Retrieval")
            
            # Sample queries
            sample_queries = [
                "What are the conclusions in this document?",
                "What are the main contributions of this paper?",
                "What methodology is used in this research?"
            ]
            
            selected_query = st.selectbox(
                "Choose a sample query or write your own:",
                ["Custom query"] + sample_queries,
                key="rag_query_select"
            )
            
            if selected_query == "Custom query":
                query = st.text_area(
                    "Enter your query:",
                    height=80,
                    key="rag_custom_query",
                    placeholder="Type your query here..."
                )
            else:
                query = st.text_area(
                    "Enter your query:",
                    value=selected_query,
                    height=80,
                    key="rag_query"
                )
            
            if st.button("🔍 Perform Tree Search", type="primary", key="tree_search", disabled=not query):
                with st.spinner("Performing reasoning-based retrieval..."):
                    try:
                        tree = st.session_state['rag_tree']
                        
                        # Remove text field for tree search
                        tree_without_text = utils.remove_fields(tree.copy(), fields=['text'])
                        
                        # Create search prompt
                        search_prompt = f"""
You are given a question and a tree structure of a document.
Each node contains a node id, node title, and a corresponding summary.
Your task is to find all nodes that are likely to contain the answer to the question.

Question: {query}

Document tree structure:
{json.dumps(tree_without_text, indent=2)}

Please reply in the following JSON format:
{{
    "thinking": "<Your thinking process on which nodes are relevant to the question>",
    "node_list": ["node_id_1", "node_id_2", ..., "node_id_n"]
}}

Directly return the final JSON structure. Do not output anything else.
"""
                        
                        # Call LLM
                        tree_search_result = asyncio.run(self.call_llm(search_prompt))
                        
                        # Parse result
                        try:
                            result_json = json.loads(tree_search_result)
                            st.session_state['search_result'] = result_json
                            st.session_state['current_query'] = query
                            
                            # Display reasoning
                            st.markdown("**🧠 Reasoning Process:**")
                            st.info(result_json['thinking'])
                            
                            # Display retrieved nodes
                            st.markdown("**📑 Retrieved Nodes:**")
                            node_map = utils.create_node_mapping(tree)
                            
                            for node_id in result_json["node_list"]:
                                if node_id in node_map:
                                    node = node_map[node_id]
                                    st.markdown(f"- **Node ID:** `{node['node_id']}` | **Page:** {node['page_index']} | **Title:** {node['title']}")
                            
                            st.success("✅ Tree search completed!")
                        
                        except json.JSONDecodeError:
                            st.error("❌ Failed to parse LLM response as JSON")
                            st.code(tree_search_result)
                    
                    except Exception as e:
                        st.error(f"❌ Error during tree search: {str(e)}")
        
        # Step 4: Answer Generation
        if 'search_result' in st.session_state:
            st.markdown("---")
            st.subheader("💡 Step 4: Generate Answer")
            
            if st.button("✨ Generate Answer", type="primary", key="generate_answer"):
                with st.spinner("Generating answer..."):
                    try:
                        tree = st.session_state['rag_tree']
                        search_result = st.session_state['search_result']
                        query = st.session_state['current_query']
                        
                        # Extract relevant content
                        node_map = utils.create_node_mapping(tree)
                        node_list = search_result["node_list"]
                        
                        relevant_content = "\n\n".join(
                            node_map[node_id]["text"] 
                            for node_id in node_list 
                            if node_id in node_map
                        )
                        
                        # Display retrieved context
                        with st.expander("📄 Retrieved Context (Preview)"):
                            preview = relevant_content[:1000] + "..." if len(relevant_content) > 1000 else relevant_content
                            st.text(preview)
                        
                        # Generate answer
                        answer_prompt = f"""
Answer the question based on the context:

Question: {query}
Context: {relevant_content}

Provide a clear, concise answer based only on the context provided.
"""
                        
                        answer = asyncio.run(self.call_llm(answer_prompt))
                        
                        st.markdown("**📝 Generated Answer:**")
                        st.success(answer)
                        
                        # Store in history
                        if 'rag_history' not in st.session_state:
                            st.session_state['rag_history'] = []
                        
                        st.session_state['rag_history'].append({
                            'query': query,
                            'reasoning': search_result['thinking'],
                            'nodes': search_result['node_list'],
                            'answer': answer
                        })
                    
                    except Exception as e:
                        st.error(f"❌ Error generating answer: {str(e)}")
            
            # Display history
            if 'rag_history' in st.session_state and st.session_state['rag_history']:
                st.markdown("---")
                st.subheader("📜 RAG History")
                
                for i, item in enumerate(reversed(st.session_state['rag_history'])):
                    with st.expander(f"Query {len(st.session_state['rag_history']) - i}: {item['query'][:50]}..."):
                        st.markdown(f"**Query:** {item['query']}")
                        st.markdown(f"**Reasoning:** {item['reasoning']}")
                        st.markdown(f"**Retrieved Nodes:** {', '.join(item['nodes'])}")
                        st.markdown(f"**Answer:** {item['answer']}")
    
    def _format_tree(self, tree, indent=0):
        """Format tree structure for display"""
        result = []
        prefix = "  " * indent
        
        if isinstance(tree, dict):
            node_id = tree.get('node_id', 'N/A')
            title = tree.get('title', 'Untitled')
            page = tree.get('page_index', 'N/A')
            
            result.append(f"{prefix}[{node_id}] {title} (Page: {page})")
            
            if 'children' in tree:
                for child in tree['children']:
                    result.append(self._format_tree(child, indent + 1))
        
        return "\n".join(result)

# Made with Bob
