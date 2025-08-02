import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from uuid import uuid4

class FAISSVectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.metadatas = []
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        
    def add_documents(self, texts, metadatas=None):
        """Add documents to the vector store"""
        if not texts:
            return
            
        # Generate embeddings
        embeddings = self.embedder.encode(texts, show_progress_bar=True)
        
        # Initialize index if not exists
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.dimension)
            
        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))
        
        # Store documents and metadata
        self.documents.extend(texts)
        if metadatas:
            self.metadatas.extend(metadatas)
        else:
            self.metadatas.extend([{"file": "unknown", "chunk_number": i+1} for i in range(len(texts))])
            
        print(f"[INFO] Added {len(texts)} documents to FAISS vector store")
        
    def search(self, query, top_k=5):
        """Search for similar documents"""
        if self.index is None or len(self.documents) == 0:
            return [], []
            
        # Encode query
        query_embedding = self.embedder.encode([query])
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), min(top_k, len(self.documents)))
        
        # Get results
        results = []
        result_metadatas = []
        
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])
                result_metadatas.append(self.metadatas[idx])
                
        return results, result_metadatas
        
    def clear(self):
        """Clear all data"""
        self.index = None
        self.documents = []
        self.metadatas = []
        print("[INFO] Cleared FAISS vector store")
        
    def save(self, filepath):
        """Save the vector store to disk"""
        if self.index is not None:
            data = {
                'index': faiss.serialize_index(self.index),
                'documents': self.documents,
                'metadatas': self.metadatas
            }
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            print(f"[INFO] Saved FAISS vector store to {filepath}")
            
    def load(self, filepath):
        """Load the vector store from disk"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            self.index = faiss.deserialize_index(data['index'])
            self.documents = data['documents']
            self.metadatas = data['metadatas']
            print(f"[INFO] Loaded FAISS vector store from {filepath}")

# Global vector store instance
vector_store = FAISSVectorStore() 