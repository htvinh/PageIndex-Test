# API Reference

Complete API reference for the PageIndex Testing Application.

## 📋 Table of Contents

- [PageIndex Client](#pageindex-client)
- [Ollama Client](#ollama-client)
- [Demo Modules](#demo-modules)
- [Utility Functions](#utility-functions)

## 🔷 PageIndex Client

The PageIndex client provides access to the PageIndex API for document processing and retrieval.

### Initialization

```python
from pageindex import PageIndexClient

client = PageIndexClient(api_key="your_api_key")
```

**Parameters:**
- `api_key` (str): Your PageIndex API key from https://dash.pageindex.ai/api-keys

### Methods

#### submit_document()

Submit a document for processing.

```python
result = client.submit_document(file_path)
doc_id = result["doc_id"]
```

**Parameters:**
- `file_path` (str): Path to the PDF document

**Returns:**
- `dict`: Contains `doc_id` for tracking the document

**Example:**
```python
doc_id = client.submit_document("path/to/document.pdf")["doc_id"]
print(f"Document ID: {doc_id}")
```

#### get_document()

Get document information and processing status.

```python
doc_info = client.get_document(doc_id)
```

**Parameters:**
- `doc_id` (str): Document ID from submit_document()

**Returns:**
- `dict`: Document information including:
  - `status`: "processing", "completed", or "failed"
  - `pageNum`: Number of pages (when completed)
  - Other metadata

**Example:**
```python
doc_info = client.get_document(doc_id)
if doc_info['status'] == 'completed':
    print(f"Document ready with {doc_info['pageNum']} pages")
```

#### is_retrieval_ready()

Check if document is ready for retrieval operations.

```python
is_ready = client.is_retrieval_ready(doc_id)
```

**Parameters:**
- `doc_id` (str): Document ID

**Returns:**
- `bool`: True if ready for retrieval

**Example:**
```python
if client.is_retrieval_ready(doc_id):
    tree = client.get_tree(doc_id)
```

#### get_tree()

Get the PageIndex tree structure of a document.

```python
tree = client.get_tree(doc_id, node_summary=True)['result']
```

**Parameters:**
- `doc_id` (str): Document ID
- `node_summary` (bool): Include node summaries (default: False)

**Returns:**
- `dict`: Tree structure with nodes containing:
  - `node_id`: Unique node identifier
  - `title`: Node title
  - `page_index`: Page number
  - `text`: Node content
  - `summary`: Node summary (if node_summary=True)
  - `children`: List of child nodes

**Example:**
```python
tree = client.get_tree(doc_id, node_summary=True)['result']
print(f"Root node: {tree['title']}")
```

#### chat_completions()

Chat with a document using streaming responses.

```python
for chunk in client.chat_completions(
    messages=[{"role": "user", "content": "Your question"}],
    doc_id=doc_id,
    stream=True
):
    print(chunk, end='', flush=True)
```

**Parameters:**
- `messages` (list): List of message dicts with 'role' and 'content'
- `doc_id` (str): Document ID
- `stream` (bool): Enable streaming (default: False)

**Returns:**
- Generator yielding response chunks (if stream=True)
- Complete response (if stream=False)

**Example:**
```python
# Streaming
full_response = ""
for chunk in client.chat_completions(
    messages=[{"role": "user", "content": "What is the main topic?"}],
    doc_id=doc_id,
    stream=True
):
    full_response += chunk
    print(chunk, end='', flush=True)

# Non-streaming
response = client.chat_completions(
    messages=[{"role": "user", "content": "Summarize this document"}],
    doc_id=doc_id,
    stream=False
)
```

## 🤖 Ollama Client

Custom client for interacting with local Ollama instance.

### Initialization

```python
from modules.ollama_client import OllamaClient

client = OllamaClient(
    base_url="http://localhost:11434",
    model="granite3-dense:8b"
)
```

**Parameters:**
- `base_url` (str): Ollama server URL (default: "http://localhost:11434")
- `model` (str): Model name (default: "granite3-dense:8b")

### Methods

#### check_connection()

Check if Ollama is running and accessible.

```python
is_connected = client.check_connection()
```

**Returns:**
- `bool`: True if Ollama is accessible

**Example:**
```python
if not client.check_connection():
    print("Ollama is not running!")
```

#### list_models()

List available models in Ollama.

```python
models = client.list_models()
```

**Returns:**
- `list`: List of model names

**Example:**
```python
models = client.list_models()
print(f"Available models: {', '.join(models)}")
```

#### generate()

Generate text completion.

```python
response = client.generate(
    prompt="Your prompt here",
    temperature=0.0,
    stream=False
)
```

**Parameters:**
- `prompt` (str): Input prompt
- `temperature` (float): Sampling temperature (0.0-1.0)
- `stream` (bool): Enable streaming

**Returns:**
- `str`: Generated text

**Example:**
```python
response = client.generate(
    prompt="Explain quantum computing in simple terms",
    temperature=0.7
)
print(response)
```

#### chat_completion()

Chat completion with message history (async).

```python
response = await client.chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.0
)
```

**Parameters:**
- `messages` (list): List of message dicts
- `temperature` (float): Sampling temperature
- `stream` (bool): Enable streaming

**Returns:**
- `str`: Generated response

**Example:**
```python
import asyncio

async def chat():
    response = await client.chat_completion(
        messages=[{"role": "user", "content": "What is AI?"}]
    )
    print(response)

asyncio.run(chat())
```

#### chat_with_vision()

Chat with vision support for multimodal models.

```python
response = client.chat_with_vision(
    prompt="Describe this image",
    image_paths=["path/to/image.jpg"],
    temperature=0.0
)
```

**Parameters:**
- `prompt` (str): Text prompt
- `image_paths` (list): List of image file paths
- `temperature` (float): Sampling temperature

**Returns:**
- `str`: Generated response

**Example:**
```python
response = client.chat_with_vision(
    prompt="What objects are in this image?",
    image_paths=["image1.jpg", "image2.jpg"]
)
print(response)
```

## 📦 Demo Modules

### ChatQuickstartDemo

Simple document Q&A demo.

```python
from modules.chat_quickstart import ChatQuickstartDemo

demo = ChatQuickstartDemo(
    api_key="your_api_key",
    ollama_url="http://localhost:11434",
    ollama_model="granite3-dense:8b"
)

# Render in Streamlit
demo.render()
```

**Methods:**
- `render()`: Render the demo UI in Streamlit

### SimpleRAGDemo

Reasoning-based RAG demo.

```python
from modules.simple_rag import SimpleRAGDemo

demo = SimpleRAGDemo(
    api_key="your_api_key",
    ollama_url="http://localhost:11434",
    ollama_model="granite3-dense:8b"
)

# Render in Streamlit
demo.render()
```

**Methods:**
- `render()`: Render the demo UI in Streamlit
- `call_llm(prompt, temperature)`: Call LLM with prompt (async)

### VisionRAGDemo

Vision-based RAG demo.

```python
from modules.vision_rag import VisionRAGDemo

demo = VisionRAGDemo(
    api_key="your_api_key",
    ollama_url="http://localhost:11434",
    ollama_model="llava"  # Vision-capable model
)

# Render in Streamlit
demo.render()
```

**Methods:**
- `render()`: Render the demo UI in Streamlit
- `extract_pdf_page_images(pdf_path, output_dir)`: Extract page images
- `get_page_images_for_nodes(node_list, node_map, page_images)`: Get images for nodes
- `call_vlm(prompt, image_paths)`: Call vision LLM (async)

## 🛠️ Utility Functions

### PageIndex Utils

```python
import pageindex.utils as utils
```

#### print_tree()

Print tree structure in readable format.

```python
utils.print_tree(tree, exclude_fields=['text'])
```

**Parameters:**
- `tree` (dict): Tree structure
- `exclude_fields` (list): Fields to exclude from display

#### remove_fields()

Remove specified fields from tree.

```python
tree_without_text = utils.remove_fields(tree.copy(), fields=['text'])
```

**Parameters:**
- `tree` (dict): Tree structure
- `fields` (list): Fields to remove

**Returns:**
- `dict`: Modified tree

#### create_node_mapping()

Create a mapping of node IDs to nodes.

```python
node_map = utils.create_node_mapping(tree, include_page_ranges=True, max_page=100)
```

**Parameters:**
- `tree` (dict): Tree structure
- `include_page_ranges` (bool): Include page range info
- `max_page` (int): Maximum page number

**Returns:**
- `dict`: Mapping of node_id to node info

**Example:**
```python
node_map = utils.create_node_mapping(tree)
node = node_map['node_123']
print(f"Node title: {node['title']}")
```

#### print_wrapped()

Print text with word wrapping.

```python
utils.print_wrapped(text, width=80)
```

**Parameters:**
- `text` (str): Text to print
- `width` (int): Maximum line width

## 📝 Data Structures

### Tree Node Structure

```python
{
    "node_id": "unique_identifier",
    "title": "Node Title",
    "page_index": 1,
    "text": "Full text content of the node",
    "summary": "Summary of the node content",
    "children": [
        # List of child nodes with same structure
    ]
}
```

### Message Structure

```python
{
    "role": "user",  # or "system", "assistant"
    "content": "Message content"
}
```

### Document Info Structure

```python
{
    "doc_id": "document_identifier",
    "status": "completed",  # or "processing", "failed"
    "pageNum": 42,
    "created_at": "2025-01-01T00:00:00Z",
    # Additional metadata
}
```

## 🔐 Environment Variables

Access via `os.getenv()`:

```python
import os

api_key = os.getenv("PAGEINDEX_API_KEY")
ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ollama_model = os.getenv("OLLAMA_MODEL", "granite3-dense:8b")
```

## ⚠️ Error Handling

### Common Exceptions

```python
try:
    doc_id = client.submit_document("document.pdf")["doc_id"]
except Exception as e:
    print(f"Error: {str(e)}")
```

### Recommended Error Handling

```python
import time

def submit_with_retry(client, file_path, max_retries=3):
    """Submit document with retry logic"""
    for attempt in range(max_retries):
        try:
            result = client.submit_document(file_path)
            return result["doc_id"]
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e

def wait_for_completion(client, doc_id, timeout=300):
    """Wait for document processing to complete"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        doc_info = client.get_document(doc_id)
        status = doc_info.get('status')
        
        if status == 'completed':
            return True
        elif status == 'failed':
            raise Exception("Document processing failed")
        
        time.sleep(5)
    
    raise TimeoutError("Document processing timeout")
```

## 📚 Examples

### Complete RAG Pipeline

```python
import asyncio
from pageindex import PageIndexClient
from modules.ollama_client import OllamaClient
import pageindex.utils as utils

async def rag_pipeline(pdf_path, query):
    # Initialize clients
    pi_client = PageIndexClient(api_key="your_key")
    ollama_client = OllamaClient()
    
    # Submit document
    doc_id = pi_client.submit_document(pdf_path)["doc_id"]
    print(f"Document submitted: {doc_id}")
    
    # Wait for processing
    while not pi_client.is_retrieval_ready(doc_id):
        time.sleep(5)
    
    # Get tree
    tree = pi_client.get_tree(doc_id, node_summary=True)['result']
    
    # Search tree
    tree_without_text = utils.remove_fields(tree.copy(), fields=['text'])
    search_prompt = f"""
    Find nodes relevant to: {query}
    Tree: {json.dumps(tree_without_text, indent=2)}
    Return JSON: {{"node_list": ["id1", "id2"]}}
    """
    
    search_result = ollama_client.generate(search_prompt)
    node_list = json.loads(search_result)["node_list"]
    
    # Extract content
    node_map = utils.create_node_mapping(tree)
    content = "\n\n".join(node_map[nid]["text"] for nid in node_list)
    
    # Generate answer
    answer_prompt = f"Question: {query}\nContext: {content}\nAnswer:"
    answer = ollama_client.generate(answer_prompt)
    
    return answer

# Run
answer = asyncio.run(rag_pipeline("document.pdf", "What is the main topic?"))
print(answer)
```

---

For more examples, see the demo modules in `modules/` directory.