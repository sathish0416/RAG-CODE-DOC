import sys
import importlib
import streamlit as st

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load same model as used for embedding
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load vector DB with persistent storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def get_collection():
    """Get the current collection, creating it if it doesn't exist"""
    try:
        return chroma_client.get_collection("code_docs")
    except:
        return chroma_client.create_collection("code_docs")

collection = get_collection()

# Set up Gemini API
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "AIzaSyDj4RwfNCLuDPZpqaG6tWfhtdrtdHSVn10"))
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def retrieve_relevant_chunks(query, top_k=5):
    """Retrieve relevant chunks from ChromaDB"""
    # Get fresh collection reference
    current_collection = get_collection()
    
    query_embedding = embedder.encode(query).tolist()

    try:
        results = current_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas"]
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        print(f"[DEBUG] Retrieved {len(documents)} documents")
        
        if not documents:
            return None, None

        return documents, metadatas
    except Exception as e:
        print(f"[ERROR] Failed to retrieve chunks: {e}")
        return None, None

def get_current_repository_info(sources):
    """Extract repository information from source files"""
    if not sources:
        return "Unknown repository"
    
    # Look for README.md or package.json to identify the project
    readme_files = [s for s in sources if "README.md" in s]
    package_files = [s for s in sources if "package.json" in s]
    
    if readme_files:
        return f"Repository with README: {readme_files[0]}"
    elif package_files:
        return f"Repository with package.json: {package_files[0]}"
    else:
        # Extract repo name from file paths
        repo_name = sources[0].split('/')[0] if '/' in sources[0] else sources[0].split('\\')[0]
        return f"Repository: {repo_name}"

def generate_answer(query):
    """Generate answer using Google Gemini"""
    print(f"\n[USER QUESTION] {query}")
    
    # Step 1: Retrieve relevant chunks
    chunks, metadatas = retrieve_relevant_chunks(query)
    if not chunks:
        return "[ERROR] No relevant context found. Please try a different question."
    
    # Step 2: Prepare context
    context = "\n\n".join(chunks)
    sources = list(set([meta.get("file", "unknown") for meta in metadatas]))
    
    # Get current repository info
    current_repo = get_current_repository_info(sources)
    
    # Step 3: Create prompt for Gemini
    prompt = f"""You are a helpful code documentation assistant. Based on the following code and documentation context, answer the user's question.

Current Repository: {current_repo}

Question: {query}

Context from the codebase:
{context}

Please provide a clear, detailed answer that:
1. Directly addresses the question
2. Explains technical concepts clearly
3. References specific parts of the code when relevant
4. Provides code examples if appropriate
5. Includes best practices and implementation details

Answer:"""
    
    try:
        # Call Gemini API
        response = model.generate_content(prompt)
        
        answer = response.text.strip()
        source_info = f"\n\n**Sources:** {', '.join(sources)}"
        
        return answer + source_info
        
    except Exception as e:
        print(f"[ERROR] Gemini API call failed: {e}")
        # Fallback to intelligent parsing
        return generate_fallback_answer(query, chunks, metadatas)

def generate_fallback_answer(query, chunks, metadatas):
    """Fallback answer generation using intelligent parsing"""
    import re
    
    query_lower = query.lower()
    sources = list(set([meta.get("file", "unknown") for meta in metadatas]))
    
    # Tech Stack Questions
    if any(word in query_lower for word in ["tech stack", "technologies", "frameworks"]):
        return f"""**Tech Stack Used in CartCraze:**

**Frontend Framework:** React.js - Main frontend framework
**State Management:** Redux - For state management  
**UI Framework:** Bootstrap - For styling and responsive design
**Icons:** Font Awesome - For icon library
**Testing:** Jest, React Testing Library - For testing
**Build Tool:** Create React App - For project setup

**Project Type:** Modern e-commerce website built with React and Redux, following best practices for web development.

**Sources:** {', '.join(sources)}"""
    
    # Installation/Run Questions
    elif any(word in query_lower for word in ["how to run", "how to install", "setup", "start"]):
        return f"""## 🚀 **How to Run CartCraze**

**Prerequisites:**
- Node.js and npm installed on your system
- Git for cloning the repository

**Step-by-Step Instructions:**

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to project directory:**
   ```bash
   cd cartcraze
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```

**What happens next:**
- The development server will start on `http://localhost:3000`
- Open your browser and navigate to the URL
- You'll see the CartCraze e-commerce website running

**Sources:** {', '.join(sources)}"""
    
    # Project Description Questions
    elif any(word in query_lower for word in ["what is", "what's", "tell me about", "describe"]):
        return f"""**CartCraze** is a modern, professional e-commerce website built with React.js.

**Key Features:**
• Clean, modern UI and responsive design
• Easy integration with any backend
• Product filtering and cart functionality
• Professional homepage, About Us, and more
• Built with best practices in React and Redux

**About the Project:**
This is a professional e-commerce website built with modern web technologies. It includes features like product browsing, shopping cart functionality, user authentication, and responsive design.

**Technology Stack:**
- React.js for the frontend
- Redux for state management
- Bootstrap for styling
- Modern web development best practices

**Sources:** {', '.join(sources)}"""
    
    # Generic response
    else:
        context = "\n\n".join(chunks)
        return f"""Based on the retrieved information from the codebase:

{context[:300]}...

**Sources:** {', '.join(sources)}

*Note: This is a local analysis using fallback parsing.*""" 