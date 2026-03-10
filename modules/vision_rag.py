"""
Vision RAG Demo Module
Based on vision_RAG_pageindex.ipynb
"""

import streamlit as st
import json
import asyncio
import fitz  # PyMuPDF
import base64
from pathlib import Path
from pageindex import PageIndexClient
import pageindex.utils as utils
from .ollama_client import OllamaClient


class VisionRAGDemo:
    """Demo for Vision-based Vectorless RAG with PageIndex"""
    
    def __init__(self, api_key: str, ollama_url: str, ollama_model: str):
        """
        Initialize Vision RAG Demo
        
        Args:
            api_key: PageIndex API key
            ollama_url: Ollama base URL
            ollama_model: Ollama model name (should support vision)
        """
        self.api_key = api_key
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.pi_client = PageIndexClient(api_key=api_key)
        self.ollama_client = OllamaClient(base_url=ollama_url, model=ollama_model)
    
    def extract_pdf_page_images(self, pdf_path: str, output_dir: str = "pdf_images") -> tuple:
        """Extract page images from PDF"""
        Path(output_dir).mkdir(exist_ok=True)
        pdf_document = fitz.open(pdf_path)
        page_images = {}
        total_pages = len(pdf_document)
        
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("jpeg")
            image_path = Path(output_dir) / f"page_{page_number + 1}.jpg"
            
            with open(image_path, "wb") as image_file:
                image_file.write(img_data)
            
            page_images[page_number + 1] = str(image_path)
        
        pdf_document.close()
        return page_images, total_pages
    
    def get_page_images_for_nodes(self, node_list: list, node_map: dict, page_images: dict) -> list:
        """Get PDF page images for retrieved nodes"""
        image_paths = []
        seen_pages = set()
        
        for node_id in node_list:
            if node_id not in node_map:
                continue
            
            node_info = node_map[node_id]
            start_page = node_info.get('start_index', node_info.get('page_index', 1))
            end_page = node_info.get('end_index', start_page)
            
            for page_num in range(start_page, end_page + 1):
                if page_num not in seen_pages and page_num in page_images:
                    image_paths.append(page_images[page_num])
                    seen_pages.add(page_num)
        
        return image_paths
    
    async def call_vlm(self, prompt: str, image_paths: list = None) -> str:
        """Call Vision Language Model using Ollama"""
        return self.ollama_client.chat_with_vision(prompt, image_paths)
    
    def render(self):
        """Render the demo UI"""
        st.markdown("---")
        
        # Check Ollama connection
        if not self.ollama_client.check_connection():
            st.error("⚠️ Cannot connect to Ollama. Please ensure Ollama is running.")
            st.info(f"Expected URL: {self.ollama_url}")
            return
        
        st.success(f"✅ Connected to Ollama ({self.ollama_model})")
        st.warning("⚠️ Note: Vision RAG requires a vision-capable model like llava or bakllava")
        
        # Step 1: Document Upload
        st.subheader("📄 Step 1: Upload Document")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type=['pdf'],
                key="vision_rag_upload",
                help="Upload a PDF document for vision-based RAG analysis"
            )
        
        with col2:
            use_sample = st.checkbox("Use sample document", value=False, key="vision_rag_sample")
            if use_sample:
                st.info("Using 'Attention Is All You Need' paper")
        
        if st.button("📤 Submit Document", type="primary", key="vision_rag_submit", disabled=not (uploaded_file or use_sample)):
            with st.spinner("Processing document..."):
                try:
                    if use_sample:
                        # Use sample document from input folder
                        sample_path = Path("input/1706.03762v7.pdf")
                        if sample_path.exists():
                            pdf_path = str(sample_path)
                        else:
                            st.error("Sample document not found in input folder")
                            return
                    else:
                        # Save uploaded file
                        temp_path = Path("temp") / uploaded_file.name
                        temp_path.parent.mkdir(exist_ok=True)
                        
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        pdf_path = str(temp_path)
                    
                    # Extract page images
                    st.info("Extracting page images from PDF...")
                    page_images, total_pages = self.extract_pdf_page_images(pdf_path)
                    st.success(f"✅ Extracted {len(page_images)} page images from {total_pages} pages")
                    
                    # Submit to PageIndex
                    st.info("Submitting document to PageIndex...")
                    doc_id = self.pi_client.submit_document(pdf_path)["doc_id"]
                    
                    st.session_state['vision_doc_id'] = doc_id
                    st.session_state['vision_page_images'] = page_images
                    st.session_state['vision_total_pages'] = total_pages
                    st.session_state['vision_pdf_path'] = pdf_path
                    
                    st.success(f"✅ Document submitted! Document ID: `{doc_id}`")
                    
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
        
        # Step 2: Get Tree Structure
        if 'vision_doc_id' in st.session_state:
            st.markdown("---")
            st.subheader("🌳 Step 2: Get PageIndex Tree Structure")
            
            doc_id = st.session_state['vision_doc_id']
            
            if st.button("🔄 Get Tree Structure", key="vision_get_tree"):
                with st.spinner("Fetching tree structure..."):
                    try:
                        if self.pi_client.is_retrieval_ready(doc_id):
                            tree = self.pi_client.get_tree(doc_id, node_summary=True)['result']
                            st.session_state['vision_tree'] = tree
                            
                            st.success("✅ Tree structure retrieved!")
                            
                            # Display simplified tree
                            with st.expander("📋 View Tree Structure"):
                                tree_str = self._format_tree(tree)
                                st.code(tree_str, language="text")
                        else:
                            st.warning("⏳ Document is still processing. Please wait and try again.")
                    
                    except Exception as e:
                        st.error(f"❌ Error getting tree: {str(e)}")
        
        # Step 3: Vision-Based Retrieval
        if 'vision_tree' in st.session_state:
            st.markdown("---")
            st.subheader("👁️ Step 3: Vision-Based Retrieval")
            
            # Sample queries
            sample_queries = [
                "What is the last operation in the Scaled Dot-Product Attention figure?",
                "Describe the architecture diagram in this paper.",
                "What are the key visual elements in the methodology section?"
            ]
            
            selected_query = st.selectbox(
                "Choose a sample query or write your own:",
                ["Custom query"] + sample_queries,
                key="vision_query_select"
            )
            
            if selected_query == "Custom query":
                query = st.text_area(
                    "Enter your query:",
                    height=80,
                    key="vision_custom_query",
                    placeholder="Type your query here..."
                )
            else:
                query = st.text_area(
                    "Enter your query:",
                    value=selected_query,
                    height=80,
                    key="vision_query"
                )
            
            if st.button("🔍 Perform Vision Search", type="primary", key="vision_search", disabled=not query):
                with st.spinner("Performing vision-based retrieval..."):
                    try:
                        tree = st.session_state['vision_tree']
                        
                        # Remove text field for tree search
                        tree_without_text = utils.remove_fields(tree.copy(), fields=['text'])
                        
                        # Create search prompt
                        search_prompt = f"""
You are given a question and a tree structure of a document.
Each node contains a node id, node title, and a corresponding summary.
Your task is to find all tree nodes that are likely to contain the answer to the question.

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
                        
                        # Call VLM for tree search
                        tree_search_result = asyncio.run(self.call_vlm(search_prompt))
                        
                        # Parse result
                        try:
                            result_json = json.loads(tree_search_result)
                            st.session_state['vision_search_result'] = result_json
                            st.session_state['vision_current_query'] = query
                            
                            # Display reasoning
                            st.markdown("**🧠 Reasoning Process:**")
                            st.info(result_json['thinking'])
                            
                            # Display retrieved nodes
                            st.markdown("**📑 Retrieved Nodes:**")
                            total_pages = st.session_state['vision_total_pages']
                            node_map = utils.create_node_mapping(tree, include_page_ranges=True, max_page=total_pages)
                            
                            for node_id in result_json["node_list"]:
                                if node_id in node_map:
                                    node_info = node_map[node_id]
                                    node = node_info['node']
                                    start_page = node_info.get('start_index', node.get('page_index', 1))
                                    end_page = node_info.get('end_index', start_page)
                                    page_range = start_page if start_page == end_page else f"{start_page}-{end_page}"
                                    
                                    st.markdown(f"- **Node ID:** `{node['node_id']}` | **Pages:** {page_range} | **Title:** {node['title']}")
                            
                            # Get page images for retrieved nodes
                            page_images = st.session_state['vision_page_images']
                            retrieved_images = self.get_page_images_for_nodes(
                                result_json["node_list"],
                                node_map,
                                page_images
                            )
                            
                            st.session_state['vision_retrieved_images'] = retrieved_images
                            st.success(f"✅ Retrieved {len(retrieved_images)} PDF page image(s) for visual context")
                        
                        except json.JSONDecodeError:
                            st.error("❌ Failed to parse VLM response as JSON")
                            st.code(tree_search_result)
                    
                    except Exception as e:
                        st.error(f"❌ Error during vision search: {str(e)}")
        
        # Step 4: Answer Generation with Visual Context
        if 'vision_search_result' in st.session_state and 'vision_retrieved_images' in st.session_state:
            st.markdown("---")
            st.subheader("💡 Step 4: Generate Answer with Visual Context")
            
            # Display retrieved images
            retrieved_images = st.session_state['vision_retrieved_images']
            
            with st.expander(f"🖼️ View Retrieved Page Images ({len(retrieved_images)} pages)"):
                if len(retrieved_images) > 0:
                    cols = st.columns(min(3, len(retrieved_images)))
                    for idx, img_path in enumerate(retrieved_images[:6]):  # Show max 6 images
                        with cols[idx % 3]:
                            st.image(img_path, caption=f"Page {Path(img_path).stem.split('_')[1]}", use_container_width=True)
                else:
                    st.info("No page images were retrieved. This might happen if the search didn't find relevant pages.")
            
            if st.button("✨ Generate Answer with Vision", type="primary", key="vision_generate_answer"):
                with st.spinner("Generating answer using visual context..."):
                    try:
                        query = st.session_state['vision_current_query']
                        retrieved_images = st.session_state['vision_retrieved_images']
                        
                        # Generate answer using VLM with visual context
                        answer_prompt = f"""
Answer the question based on the images of the document pages as context.

Question: {query}

Provide a clear, concise answer based only on the context provided in the images.
"""
                        
                        answer = asyncio.run(self.call_vlm(answer_prompt, retrieved_images))
                        
                        st.markdown("**📝 Generated Answer (Vision-based):**")
                        st.success(answer)
                        
                        # Store in history
                        if 'vision_history' not in st.session_state:
                            st.session_state['vision_history'] = []
                        
                        st.session_state['vision_history'].append({
                            'query': query,
                            'reasoning': st.session_state['vision_search_result']['thinking'],
                            'nodes': st.session_state['vision_search_result']['node_list'],
                            'num_images': len(retrieved_images),
                            'answer': answer
                        })
                    
                    except Exception as e:
                        st.error(f"❌ Error generating answer: {str(e)}")
            
            # Display history
            if 'vision_history' in st.session_state and st.session_state['vision_history']:
                st.markdown("---")
                st.subheader("📜 Vision RAG History")
                
                for i, item in enumerate(reversed(st.session_state['vision_history'])):
                    with st.expander(f"Query {len(st.session_state['vision_history']) - i}: {item['query'][:50]}..."):
                        st.markdown(f"**Query:** {item['query']}")
                        st.markdown(f"**Reasoning:** {item['reasoning']}")
                        st.markdown(f"**Retrieved Nodes:** {', '.join(item['nodes'])}")
                        st.markdown(f"**Images Used:** {item['num_images']} pages")
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
