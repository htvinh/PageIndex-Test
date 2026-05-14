"""
Local PageIndex Client
Mimics PageIndexClient functionality using local LLM and PyMuPDF
"""

import os
import json
import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional, Dict, Any, List
from pageindex_test.modules.llm.base import LLMProvider


class LocalPageIndexClient:
    """Local replacement for PageIndexClient"""
    
    def __init__(self, llm: LLMProvider, storage_dir: str = "_local_storage"):
        """
        Initialize Local PageIndex Client
        
        Args:
            llm: LLM provider instance for summarization and reasoning
            storage_dir: Directory to store processed document trees
        """
        self.llm = llm
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def submit_document(self, file_path: str, enable_vision: bool = False) -> Dict[str, str]:
        """
        Process a document locally.
        
        Args:
            file_path: Path to the PDF document
            enable_vision: If True, extracts images for every page.
        """
        file_path = Path(file_path)
        doc_id = file_path.stem
        
        # Check if already processed
        tree_path = self.storage_dir / f"{doc_id}.json"
        if tree_path.exists():
            return {"doc_id": doc_id}
        
        # Create output dir for images if vision enabled
        image_dir = self.storage_dir / doc_id / "images"
        if enable_vision:
            image_dir.mkdir(parents=True, exist_ok=True)
        
        # Process PDF
        pdf_doc = fitz.open(str(file_path))
        num_pages = len(pdf_doc)
        
        print(f"\n🚀 Processing document: {file_path.name} ({num_pages} pages)")
        
        pages_data = []
        
        for i in range(num_pages):
            page = pdf_doc.load_page(i)
            text = page.get_text()
            
            image_path = None
            if enable_vision:
                mat = fitz.Matrix(2.0, 2.0)
                pix = page.get_pixmap(matrix=mat)
                image_path = image_dir / f"page_{i + 1}.jpg"
                pix.save(str(image_path))
            
            # Generate summary for the page (using text)
            summary_prompt = f"""Summarize the following document page in 1-2 concise sentences. 
            CRITICAL: If the page contains numerical data (ages, limits, dates, percentages, monetary values), ensure these are preserved in the summary.

            TEXT: {text[:4000]}"""
            summary = self.llm.get_response(
                prompt=summary_prompt, 
                system="You are an assistant that creates accurate summaries. Never lose numerical constraints.",
                message=f"--- 📝 Processing Page {i+1}/{num_pages} "
            )

            
            pages_data.append({
                "node_id": f"page_{i+1}",
                "title": f"Page {i+1}",
                "page_index": i + 1,
                "text": text,
                "image_path": str(image_path) if image_path else None,
                "summary": summary,
                "children": []
            })
        
        # Build tree
        tree = {
            "node_id": "root",
            "title": file_path.name,
            "page_index": 1,
            "text": "",
            "summary": f"Document with {num_pages} pages.",
            "children": pages_data
        }
        
        # Save tree
        with open(tree_path, "w") as f:
            json.dump(tree, f, indent=2)
        
        # Save metadata
        meta_path = self.storage_dir / f"{doc_id}_meta.json"
        with open(meta_path, "w") as f:
            json.dump({
                "status": "completed",
                "pageNum": num_pages,
                "file_path": str(file_path)
            }, f, indent=2)
            
        pdf_doc.close()
        return {"doc_id": doc_id}
    
    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """Get document info"""
        meta_path = self.storage_dir / f"{doc_id}_meta.json"
        if meta_path.exists():
            with open(meta_path, "r") as f:
                return json.load(f)
        return {"status": "not_found"}
    
    def update_document(self, file_path: str, enable_vision: bool = False) -> Dict[str, str]:
        """Delete existing index data and re-process."""
        file_path = Path(file_path)
        doc_id = file_path.stem
        
        # Remove existing
        tree_path = self.storage_dir / f"{doc_id}.json"
        meta_path = self.storage_dir / f"{doc_id}_meta.json"
        image_dir = self.storage_dir / doc_id / "images"
        
        if tree_path.exists(): tree_path.unlink()
        if meta_path.exists(): meta_path.unlink()
        import shutil
        if image_dir.exists(): shutil.rmtree(image_dir)
            
        return self.submit_document(str(file_path), enable_vision)
    
    def get_tree(self, doc_id: str, node_summary: bool = True) -> Dict[str, Any]:
        """Get the document tree"""
        tree_path = self.storage_dir / f"{doc_id}.json"
        if tree_path.exists():
            with open(tree_path, "r") as f:
                tree = json.load(f)
                return {"result": tree}
        return {"result": None}

    def get_manifest(self) -> List[Dict[str, Any]]:
        """Return a manifest of all processed documents"""
        manifest = []
        for meta_path in self.storage_dir.glob("*_meta.json"):
            with open(meta_path, "r") as f:
                data = json.load(f)
                doc_id = meta_path.name.replace("_meta.json", "")
                data["doc_id"] = doc_id
                # Get the tree title
                tree_path = self.storage_dir / f"{doc_id}.json"
                if tree_path.exists():
                    with open(tree_path, "r") as f:
                        tree = json.load(f)
                        data["title"] = tree.get("title", doc_id)
                manifest.append(data)
        return manifest

