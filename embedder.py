import sys
import importlib

# embedder.py

from vector_store import vector_store
from uuid import uuid4

# Define the embedding model name
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def add_chunks_to_db(chunks, source_file=None):
    """
    Adds a list of text chunks to the FAISS vector store.

    Args:
        chunks (List[str]): The list of text chunks.
        source_file (str): Optional. The source file path for metadata.
    """

    if not chunks:
        print(f"[WARNING] No chunks to embed for file: {source_file}")
        return

    # Metadata helps in filtering/debugging later
    metadatas = [
        {"file": source_file.replace('\\', '/') if source_file else "unknown", "chunk_number": i + 1}
        for i in range(len(chunks))
    ]

    try:
        # Add to FAISS vector store
        vector_store.add_documents(chunks, metadatas)
        print(f"[INFO] Stored {len(chunks)} chunks from {source_file or 'unknown source'} into FAISS vector store.")

    except Exception as e:
        print(f"[ERROR] Failed to store chunks for {source_file}: {e}")

def clear_database():
    """Clear all data from FAISS vector store"""
    vector_store.clear()
    print("[INFO] Cleared FAISS vector store")
