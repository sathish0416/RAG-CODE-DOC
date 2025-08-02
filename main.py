# main.py

from utils import clone_repo, get_code_files
from chunker import chunk_python_code, chunk_markdown, chunk_generic_code
from embedder import add_chunks_to_db
import uuid
import os

def process_repository(repo_url):
    """Process a GitHub repository for RAG system"""
    print(f"Processing repository: {repo_url}")
    
    # Clear previous data from ChromaDB
    from embedder import clear_database
    clear_database()
    print("✅ Cleared previous repository data")
    
    # Clone the repository
    repo_path = clone_repo(repo_url)
    if not repo_path:
        print("Failed to clone repository")
        return False
    
    # Get code files
    files = get_code_files("repo")
    print(f"Found {len(files)} files to process")
    
    # Process each file
    for file in files:
        print(f"Processing: {file}")
        
        # Chunk the file based on its type
        if file.endswith(".py"):
            chunks = chunk_python_code(file)
        elif file.endswith((".md", ".txt")):
            chunks = chunk_markdown(file)
        elif file.endswith((".js", ".jsx")):
            chunks = chunk_generic_code(file)
        else:
            chunks = chunk_generic_code(file)
        
        if chunks:
            # Add chunks to database
            add_chunks_to_db(chunks, source_file=file)
            print(f"Added {len(chunks)} chunks from {file}")
    
    print("Repository processing completed!")
    return True

if __name__ == "__main__":
    # Get repository URL from user input
    repo_url = input("Enter GitHub repository URL: ")
    
    if not repo_url:
        print("No repository URL provided. Exiting.")
        exit(1)
    
    # Process the repository
    success = process_repository(repo_url)
    
    if success:
        print("✅ Repository processing completed successfully!")
    else:
        print("❌ Repository processing failed!")
