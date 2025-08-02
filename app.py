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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .code-block {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 RAG Code Documentation Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask questions about any GitHub repository and get intelligent answers!</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Repository input
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository.git",
            help="Enter the full GitHub repository URL"
        )
        
        # Process repository button
        if st.button("🔄 Process Repository", type="primary"):
            if repo_url:
                with st.spinner("Processing repository..."):
                    try:
                        # Process the repository
                        process_repository(repo_url)
                        st.success("✅ Repository processed successfully!")
                        st.session_state.repo_processed = True
                        st.session_state.repo_url = repo_url
                    except Exception as e:
                        st.error(f"❌ Error processing repository: {str(e)}")
            else:
                st.warning("⚠️ Please enter a repository URL")
        
        # Clear database button
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
        
        # Show current status
        if 'repo_processed' in st.session_state and st.session_state.repo_processed:
            st.markdown('<div class="success-box">✅ Repository Ready</div>', unsafe_allow_html=True)
            st.info(f"Current repo: {st.session_state.repo_url}")
            
            # Show repository info
            try:
                import chromadb
                client = chromadb.PersistentClient(path="./chroma_db")
                collection = client.get_collection("code_docs")
                chunk_count = collection.count()
                st.success(f"📚 {chunk_count} chunks loaded from current repository")
            except:
                st.warning("⚠️ Database status unavailable")
        
        # Sample questions
        st.header("💡 Sample Questions")
        sample_questions = [
            "What is the tech stack used?",
            "How to run the project?",
            "Explain the project structure",
            "What are the main features?",
            "How is state management implemented?",
            "Show me the authentication system"
        ]
        
        for question in sample_questions:
            if st.button(question, key=f"sample_{question}"):
                st.session_state.user_question = question
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("❓ Ask Questions")
        
        # Check if repository is processed
        if 'repo_processed' not in st.session_state or not st.session_state.repo_processed:
            st.info("👈 Please process a repository first using the sidebar")
            return
        
        # Question input
        user_question = st.text_input(
            "Your Question",
            value=st.session_state.get('user_question', ''),
            placeholder="Ask anything about the codebase...",
            key="question_input"
        )
        
        # Ask button
        if st.button("🚀 Get Answer", type="primary"):
            if user_question:
                with st.spinner("🤔 Thinking..."):
                    try:
                        # Generate answer
                        start_time = time.time()
                        answer = generate_answer(user_question)
                        end_time = time.time()
                        
                        # Display answer
                        st.markdown("### 📝 Answer")
                        st.markdown(answer)
                        
                        # Show metrics
                        response_time = end_time - start_time
                        st.info(f"⏱️ Response time: {response_time:.2f} seconds")
                        
                        # Store in session for history
                        if 'chat_history' not in st.session_state:
                            st.session_state.chat_history = []
                        
                        st.session_state.chat_history.append({
                            'question': user_question,
                            'answer': answer,
                            'timestamp': time.strftime("%H:%M:%S")
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Error generating answer: {str(e)}")
            else:
                st.warning("⚠️ Please enter a question")
    
    with col2:
        st.header("📊 System Info")
        
        # Check ChromaDB status
        try:
            import chromadb
            client = chromadb.PersistentClient(path="./chroma_db")
            collection = client.get_collection("code_docs")
            chunk_count = collection.count()
            
            st.metric("📚 Chunks Stored", chunk_count)
            
            if chunk_count > 0:
                st.success("✅ Vector Database Ready")
            else:
                st.warning("⚠️ No data in database")
                
        except Exception as e:
            st.error(f"❌ Database Error: {str(e)}")
        
        # Show chat history
        if 'chat_history' in st.session_state and st.session_state.chat_history:
            st.header("💬 Recent Questions")
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
                with st.expander(f"Q: {chat['question'][:50]}... ({chat['timestamp']})"):
                    st.write(f"**Question:** {chat['question']}")
                    st.write(f"**Answer:** {chat['answer'][:200]}...")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ using Streamlit, ChromaDB, and Google Gemini</p>
            <p>RAG Code Documentation Assistant v1.0</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 