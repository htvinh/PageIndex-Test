"""
Document Analysis Module (Local)
Unified Multimodal RAG with reasoning over text and visual context.
"""

import streamlit as st
import json
import fitz
from pathlib import Path
from pageindex_test.modules.local_pi import LocalPageIndexClient
from pageindex_test.modules.llm.base import LLMProvider


class DocAnalysisDemo:
    def __init__(self, llm: LLMProvider):
        self.llm = llm
        self.pi_client = LocalPageIndexClient(llm=llm)

    def _find_node(self, node, target_id):
        if isinstance(node, dict):
            if node.get('node_id') == target_id: return node
            for child in node.get('children', []):
                res = self._find_node(child, target_id)
                if res: return res
        return None

    def render(self):
        st.markdown("---")
        
        # Step 1: Select Documents
        st.subheader("📄 Step 1: Select Documents")
        manifest = self.pi_client.get_manifest()
        # Upload new
        uploaded_files = st.file_uploader("Upload new PDFs", type=['pdf'], key="doc_upload", accept_multiple_files=True)
        if uploaded_files and st.button("Process", key="proc_btn"):
            with st.spinner("Processing..."):
                manifest = self.pi_client.get_manifest()
                for uploaded_file in uploaded_files:
                    # Check if filename exists
                    already_indexed = any(d['title'] == uploaded_file.name for d in manifest)
                    
                    if already_indexed:
                        if not st.checkbox(f"Document '{uploaded_file.name}' is already indexed. Re-index?", key=f"reindex_{uploaded_file.name}"):
                            continue
                            
                    temp_path = Path("temp") / uploaded_file.name
                    temp_path.parent.mkdir(exist_ok=True)
                    with open(temp_path, "wb") as f: f.write(uploaded_file.getbuffer())
                    self.pi_client.submit_document(str(temp_path), enable_vision=st.session_state.get('enable_vision', False))
                    temp_path.unlink()
                    st.rerun()
        # Multi-select
        manifest = self.pi_client.get_manifest()
        selected_docs = st.multiselect(
            "Select documents to query:",
            options=[d["doc_id"] for d in manifest],
            default=[],
            format_func=lambda x: next((d["title"] for d in manifest if d["doc_id"] == x), x)
        )
        
        if not selected_docs:
            st.info("Please select one or more documents to begin analysis.")
            return
        
        trees = [self.pi_client.get_tree(doc_id)['result'] for doc_id in selected_docs]
        if st.button("🔄 Aggregate Trees"):
            st.session_state['rag_trees'] = trees
            st.success(f"✅ Aggregated {len(trees)} documents!")
        
        if 'rag_trees' in st.session_state:
            st.markdown("---")
            st.subheader("🔍 Analysis Query")
            query = st.text_area("Enter your question:", height=80, key="rag_query")
            
            if st.button("✨ Perform Analysis", type="primary", disabled=not query):
                with st.spinner("Reasoning and gathering context..."):
                    # Create a key for caching
                    query_key = f"{query}_{','.join(selected_docs)}_{st.session_state.get('enable_vision', False)}"
                    if st.session_state.get('last_query') == query_key:
                        st.info("Using cached results for this query.")
                        search_results = st.session_state['last_results']
                        relevant_content = st.session_state['last_content']
                        images = st.session_state['last_images']
                    else:
                        # Reasoning step
                        trees = st.session_state['rag_trees']
                        search_results = []
                        for tree in trees:
                            # Prune tree for search: keep only node_id, title, summary
                            def prune(node):
                                return {
                                    "id": node.get("node_id"),
                                    "title": node.get("title"),
                                    "summary": node.get("summary"),
                                    "children": [prune(c) for c in node.get("children", [])]
                                }

                            pruned_tree = prune(tree)
                            prompt = f"Question: {query}. Document: {tree.get('title')}. Identify relevant nodes. Return JSON: {{\"thinking\": \"...\", \"node_list\": [\"page_1\", ...]}}. \n\nTree: {json.dumps(pruned_tree)}"

                            res = self.llm.get_response(prompt, system="You are an expert retrieval assistant. Be concise.", message=f"--- 🔍 Searching {tree.get('title')} ")
                            try:
                                res_json = json.loads(res.replace("```json", "").replace("```", "").strip())
                                search_results.append({"tree": tree, "nodes": res_json["node_list"]})
                            except: continue

                        # Aggregate Content
                        contents = []
                        images = []
                        for res in search_results:
                            for nid in res["nodes"]:
                                node = self._find_node(res["tree"], nid)
                                if node:
                                    if node.get("text"): contents.append(f"Text from {res['tree'].get('title')}: {node['text']}")
                                    if st.session_state.get('enable_vision') and node.get("image_path"): images.append(node["image_path"])
                        relevant_content = "\n\n".join(contents)

                        # Cache results
                        st.session_state['last_query'] = query_key
                        st.session_state['last_results'] = search_results
                        st.session_state['last_content'] = relevant_content
                        st.session_state['last_images'] = images


                    # Display retrieved
                    with st.expander("📄 Retrieved Context"):
                        st.text(relevant_content[:1000] + "...")
                        if images: st.image(images[:3], width=200)

                    # Answer
                    ans = self.llm.get_response(f"Context: {relevant_content}\nQuestion: {query}", images=images, system="Multimodal analyst.")
                    st.markdown("**📝 Analysis:**")
                    st.success(ans)
