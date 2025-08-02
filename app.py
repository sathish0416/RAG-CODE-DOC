import streamlit as st
import os
import subprocess
import sys
from rag_gemini import generate_answer
from main import process_repository
import time

# Page configuration
st.set_page_config(
    page_title="RAG Code Documentation Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<h1 class="main-header">🤖 RAG Code Documentation Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="sidebar-header">⚙️ Configuration</h2>', unsafe_allow_html=True)
        
        # GitHub URL input
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository",
            help="Enter the full GitHub repository URL"
        )
        
        # Process Repository button
        if st.button("🚀 Process Repository", type="primary"):
            if repo_url:
                with st.spinner("Processing repository..."):
                    try:
                        success = process_repository(repo_url)
                        if success:
                            st.success("✅ Repository processed successfully!")
                            st.session_state.repo_processed = True
                            st.session_state.repo_url = repo_url
                        else:
                            st.error("❌ Failed to process repository")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a repository URL")
        
        # Status display
        if 'repo_processed' in st.session_state:
            st.markdown('<div class="status-box success-box">✅ Repository loaded and ready for questions!</div>', unsafe_allow_html=True)
            
            # Show chunk count
            try:
                import chromadb
                client = chromadb.PersistentClient(path="./chroma_db")
                collection = client.get_collection("code_docs")
                chunk_count = collection.count()
                st.info(f"📚 {chunk_count} chunks loaded from current repository")
            except:
                st.info("📚 Repository data loaded")
        
        # Clear Database button
        if st.button("🗑️ Clear Database", type="secondary"):
            try:
                from embedder import clear_database
                clear_database()
                st.success("✅ Database cleared successfully!")
                if 'repo_processed' in st.session_state:
                    del st.session_state.repo_processed
                if 'repo_url' in st.session_state:
                    del st.session_state.repo_url
            except Exception as e:
                st.error(f"❌ Error clearing database: {str(e)}")
        
        # Sample questions
        st.markdown('<h3 class="sidebar-header">💡 Sample Questions</h3>', unsafe_allow_html=True)
        sample_questions = [
            "What is the tech stack used?",
            "How to run the project?",
            "Explain the project structure",
            "What are the main features?",
            "How is authentication implemented?"
        ]
        
        for question in sample_questions:
            if st.button(question, key=f"sample_{question}"):
                st.session_state.user_question = question
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Ask Questions About the Codebase")
        
        # Question input
        user_question = st.text_input(
            "Your Question",
            value=st.session_state.get('user_question', ''),
            placeholder="Ask anything about the codebase...",
            key="question_input"
        )
        
        # Ask button
        if st.button("🔍 Ask Question", type="primary"):
            if user_question:
                with st.spinner("Generating answer..."):
                    start_time = time.time()
                    try:
                        answer = generate_answer(user_question)
                        end_time = time.time()
                        response_time = end_time - start_time
                        
                        # Display answer
                        st.markdown("### 📝 Answer")
                        st.markdown(answer)
                        
                        # Display response time
                        st.info(f"⏱️ Response time: {response_time:.2f} seconds")
                        
                        # Store in chat history
                        if 'chat_history' not in st.session_state:
                            st.session_state.chat_history = []
                        
                        st.session_state.chat_history.append({
                            'question': user_question,
                            'answer': answer,
                            'time': response_time
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Error generating answer: {str(e)}")
            else:
                st.warning("⚠️ Please enter a question")
        
        # Chat history
        if 'chat_history' in st.session_state and st.session_state.chat_history:
            st.markdown("### 📚 Chat History")
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {chat['question'][:50]}... ({chat['time']:.2f}s)"):
                    st.markdown(f"**Question:** {chat['question']}")
                    st.markdown(f"**Answer:** {chat['answer']}")
    
    with col2:
        st.markdown("### 📊 System Info")
        
        # ChromaDB status
        try:
            import chromadb
            client = chromadb.PersistentClient(path="./chroma_db")
            collection = client.get_collection("code_docs")
            chunk_count = collection.count()
            if chunk_count > 0:
                st.success(f"✅ {chunk_count} chunks loaded")
            else:
                st.warning("⚠️ No chunks loaded")
        except:
            st.warning("⚠️ Database status unavailable")
        
        # Repository info
        if 'repo_url' in st.session_state:
            st.info(f"📁 Repository: {st.session_state.repo_url}")
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            if 'chat_history' in st.session_state:
                del st.session_state.chat_history
            st.success("✅ Chat history cleared!")

if __name__ == "__main__":
    main() 