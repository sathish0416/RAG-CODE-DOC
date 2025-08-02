import sys
import importlib

# embedder.py

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from uuid import uuid4

# Define the embedding model name
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Initialize ChromaDB client with persistent storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="code_docs")

# Load embedding model once
embedder = SentenceTransformer(EMBEDDING_MODEL)

def add_chunks_to_db(chunks, source_file=None):
    """
    Adds a list of text chunks to the ChromaDB vector store.

    Args:
        chunks (List[str]): The list of text chunks.
        source_file (str): Optional. The source file path for metadata.
    """

    if not chunks:
        print(f"[WARNING] No chunks to embed for file: {source_file}")
        return

    # Ensure unique and safe IDs
    ids = []
    for i in range(len(chunks)):
        if source_file:
            safe_path = source_file.replace('\\', '/')
            ids.append(f"{safe_path}::{i+1}")
        else:
            ids.append(str(uuid4()))

    # Metadata helps in filtering/debugging later
    metadatas = [
        {"file": source_file.replace('\\', '/'), "chunk_number": i + 1}
        for i in range(len(chunks))
    ]

    try:
        # Generate vector embeddings
        embeddings = embedder.encode(chunks, show_progress_bar=True).tolist()

        # Get fresh collection reference
        current_collection = get_fresh_collection()

        # Add to ChromaDB
        current_collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

        print(f"[INFO] Stored {len(chunks)} chunks from {source_file or 'unknown source'} into ChromaDB.")

    except Exception as e:
        print(f"[ERROR] Failed to store chunks for {source_file}: {e}")

def get_fresh_collection():
    """Get a fresh reference to the collection"""
    try:
        return chroma_client.get_collection("code_docs")
    except:
        return chroma_client.create_collection("code_docs")

def clear_database():
    """Clear all data from ChromaDB collection"""
    try:
        # Delete the collection
        chroma_client.delete_collection("code_docs")
        print("[INFO] Deleted existing collection")
    except:
        pass
    
    # Recreate the collection
    global collection
    collection = chroma_client.create_collection("code_docs")
    print("[INFO] Created fresh collection")
