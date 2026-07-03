import os
import logging
import json
from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# Use a mock embeddings if no API key is provided, or initialize standard embeddings
# Since the prompt said Groq defaults for LLM, Groq doesn't provide standard embeddings easily yet.
# We will use a HuggingFace embedding or fake embeddings for MVP if needed.
# For simplicity, we'll try to use OpenAI if key is present, otherwise fallback.
try:
    from langchain_huggingface import HuggingFaceEmbeddings

    # Initialize SentenceTransformer embedding model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
except ImportError:
    # Fallback to Fake if HF is not installed
    from langchain_core.embeddings import FakeEmbeddings
    embeddings = FakeEmbeddings(size=384)

logger = logging.getLogger(__name__)

INDEX_PATH = "ai/memory/faiss_index"

def get_vector_store():
    if os.path.exists(INDEX_PATH):
        try:
            return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            logger.warning(f"Failed to load FAISS index: {e}")
    
    # Create empty store with a dummy document so it initializes correctly
    doc = Document(page_content="Initial memory context.", metadata={"type": "init"})
    store = FAISS.from_documents([doc], embeddings)
    store.save_local(INDEX_PATH)
    return store

def add_to_memory(text: str, metadata: Dict[str, Any]):
    """Add a new memory to the FAISS vector store."""
    store = get_vector_store()
    doc = Document(page_content=text, metadata=metadata)
    store.add_documents([doc])
    store.save_local(INDEX_PATH)

def search_memory(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """Search semantic memory."""
    store = get_vector_store()
    results = store.similarity_search(query, k=k)
    return [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]
