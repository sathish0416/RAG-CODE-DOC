# 🤖 RAG Code Documentation Assistant

A powerful Retrieval-Augmented Generation (RAG) system that can analyze any GitHub repository and answer questions about the codebase using AI.

## 🌟 Features

- **📚 Repository Analysis**: Clone and analyze any GitHub repository
- **🧠 Intelligent Q&A**: Ask questions about code, tech stack, setup instructions
- **🔍 Smart Chunking**: Intelligent code and documentation chunking
- **💾 Vector Storage**: ChromaDB for efficient document retrieval
- **🤖 AI-Powered**: Google Gemini for intelligent answer generation
- **🌐 Web Interface**: Beautiful Streamlit UI for easy interaction
- **📊 Real-time Metrics**: Response times and system status

## 🚀 Live Demo

**🌐 [Try the Live App](https://rag-code-doc-dbqfdgx5bgwsfbvcfyzvwj.streamlit.app)**

**[Deploy on Streamlit Cloud](https://share.streamlit.io/)**

## 📋 Summary of Approach

### **RAG (Retrieval-Augmented Generation) Architecture:**

1. **Repository Processing:**
   - Clone GitHub repositories using GitPython
   - Extract and process code files, documentation, and configuration files
   - Implement intelligent chunking to break down large files into meaningful segments

2. **Vector Embeddings:**
   - Use SentenceTransformers (all-MiniLM-L6-v2) for generating embeddings
   - Store embeddings in FAISS vector database for efficient similarity search
   - Maintain metadata for source attribution

3. **Question Answering:**
   - Convert user questions to embeddings
   - Retrieve most relevant code chunks using similarity search
   - Generate contextual answers using Google Gemini AI
   - Provide source attribution for transparency

4. **Web Interface:**
   - Streamlit-based user interface for easy interaction
   - Real-time processing and response generation
   - Support for multiple repository analysis

### **Key Technical Decisions:**
- **FAISS over ChromaDB:** Chose FAISS for better cloud compatibility and performance
- **SentenceTransformers:** Selected for efficient, high-quality embeddings
- **Google Gemini:** Used for intelligent, context-aware answer generation
- **Streamlit:** Chosen for rapid development and deployment

## 🔍 Assumptions Made

1. **Repository Access:**
   - Assumes public GitHub repositories (no authentication required)
   - Assumes repositories contain readable code files (not binary files)

2. **File Types:**
   - Focuses on common code file extensions (.py, .js, .html, .css, .md, etc.)
   - Assumes text-based configuration files

3. **API Limitations:**
   - Assumes Google Gemini API key is available and has sufficient quota
   - Assumes reasonable API response times

4. **Performance:**
   - Assumes repositories are of reasonable size (< 100MB)
   - Assumes single-user concurrent access (can be scaled)

5. **Data Persistence:**
   - Assumes in-memory storage is sufficient (data cleared on restart)
   - Assumes users will re-upload repositories as needed

6. **User Behavior:**
   - Assumes users will provide clear, specific questions
   - Assumes users understand basic repository structure

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **Web Framework**: Streamlit
- **Vector Database**: ChromaDB
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **AI Model**: Google Gemini API
- **Repository Handling**: GitPython

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git
- Google Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone  "https://github.com/sathish0416/RAG-CODE-DOC"
   cd rag-code-doc
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🎯 Usage

### Web Interface
1. Open the Streamlit app
2. Enter a GitHub repository URL
3. Click "Process Repository"
4. Ask questions about the codebase

### Command Line
```bash
# Process a repository
python main.py

# Ask questions
python ask.py
```

## 📁 Project Structure

```
rag-code-doc/
├── app.py                 # Streamlit web interface
├── main.py               # Repository processing
├── rag_gemini.py         # RAG system with Gemini
├── embedder.py           # Vector embeddings
├── chunker.py            # Code chunking
├── utils.py              # Repository utilities
├── ask.py                # Command line interface
├── requirements.txt      # Dependencies
├── .env                  # Environment variables
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `CHROMA_DB_PATH`: ChromaDB storage path (default: ./chroma_db)


## 🚀 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Connect your GitHub account
   - Select your repository
   - Set the main file path: `app.py`
   - Add secrets for API keys
   - Deploy!

### Environment Variables for Deployment
Add these in Streamlit Cloud secrets:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

## 🧪 Testing

### Test Commands
```bash
# Test repository processing
python main.py

# Test RAG system
python ask.py

# Test web interface
streamlit run app.py
```

### Sample Questions
- "What is the tech stack used?"
- "How to run the project?"
- "Explain the project structure"
- "What are the main features?"
- "How is authentication implemented?"

## 📊 Performance

- **Response Time**: < 10 seconds
- **Supported Repositories**: Any public GitHub repo
- **Chunking Quality**: Intelligent code-aware splitting
- **Answer Quality**: Context-aware, source-attributed responses

## 🔒 Security

- API keys stored in environment variables
- No sensitive data in code
- Secure repository cloning
- Input validation and sanitization

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Streamlit for the web framework
- ChromaDB for vector storage
- SentenceTransformers for embeddings


**Built using Streamlit, ChromaDB, and Google Gemini** 