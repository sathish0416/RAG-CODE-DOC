# check_chromadb.py

import chromadb
from chromadb.config import Settings

# Connect to ChromaDB with persistent storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("code_docs")

# Get all documents
results = collection.get(include=["documents", "metadatas"])

documents = results.get("documents", [])
metadatas = results.get("metadatas", [])

print(f"\n[INFO] Total Chunks in ChromaDB: {len(documents)}\n")

# Group by file source
file_counts = {}
for metadata in metadatas:
    file_path = metadata.get("file", "unknown")
    file_counts[file_path] = file_counts.get(file_path, 0) + 1

print("[FILE BREAKDOWN]:")
for file_path, count in file_counts.items():
    print(f"  {file_path}: {count} chunks")

print(f"\n[FIRST 3 CHUNKS PREVIEW]:")
for i, (doc, metadata) in enumerate(zip(documents[:3], metadatas[:3])):
    print(f"\n[Chunk {i+1}] - Source: {metadata.get('file', 'unknown')}")
    print(f"Content: {doc[:200]}...")
    print("-" * 80) 