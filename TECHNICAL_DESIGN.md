# Technical Design Document
## Project 1: AI Research Assistant (RAG)

### 1. Overview

The AI Research Assistant is a Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask questions about their content. The system uses OpenAI embeddings for semantic search and GPT-3.5 for natural language answers.

### 2. Architecture

**High-Level Architecture**

**Component Diagram**
┌────────────────────────────────────────────────────────────────┐
│ Streamlit UI (rag_app.py) │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ PDF Upload │ Chat Interface │ Settings │ │
│ └───────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────────────┐
│ QA Engine (qa_engine.py) │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ ask() │ retrieve_context() │ generate_answer() │ │
│ └───────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────────────┐
│ Embeddings Manager (embeddings_manager.py) │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ add_chunks() │ search() │ get_stats() │ │
│ └───────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────────────┐
│ ChromaDB Vector Database │
└────────────────────────────────────────────────────────────────┘

text

### 3. Components

**Component 1: PDF Processor (`pdf_processor.py`)**
- Purpose: Extract text from PDF files
- Key functions: `load_pdf()`, `split_text_into_chunks()`
- Dependencies: PyPDFLoader, langchain-community

**Component 2: Embeddings Manager (`embeddings_manager.py`)**
- Purpose: Generate embeddings and manage vector storage
- Key functions: `add_chunks()`, `search()`
- Dependencies: OpenAI, ChromaDB

**Component 3: QA Engine (`qa_engine.py`)**
- Purpose: Retrieve context and generate answers
- Key functions: `ask()`, `generate_answer()`
- Dependencies: OpenAI GPT-3.5

**Component 4: RAG Pipeline (`rag_pipeline.py`)**
- Purpose: Orchestrate the full RAG workflow
- Key functions: `process_pdf_and_store()`, `process_multiple_pdfs()`

**Component 5: Streamlit UI (`rag_app.py`)**
- Purpose: User interface for document upload and chat
- Key features: PDF upload, chat interface, progress indicators

**Component 6: Cost Tracker (`cost_tracker.py`)**
- Purpose: Track API usage and costs
- Key features: Token counting, cost calculation

### 4. Data Flow

1. User uploads a PDF file
2. PDF is loaded and text is extracted using PyPDFLoader
3. Text is split into overlapping chunks (500 characters, 50 overlap)
4. Each chunk is converted to an embedding using OpenAI's ada-002 model
5. Embeddings are stored in ChromaDB
6. User enters a question
7. The question is embedded and used for semantic search
8. Relevant chunks are retrieved from ChromaDB
9. Retrieved chunks are provided as context to GPT-3.5
10. GPT generates a natural language answer
11. Answer is displayed to the user with sources

### 5. Technologies Used

**Python Libraries:**
- OpenAI API – Embeddings and GPT-3.5
- ChromaDB – Vector database
- LangChain – PDF loading and document processing
- PyPDFLoader – PDF text extraction
- Streamlit – User interface
- python-dotenv – Environment variables
- Plotly – Data visualization (planned)
- Pandas – Data processing (planned)

### 6. API Integration

**OpenAI API**
- Model for Chat: gpt-3.5-turbo
- Model for Embeddings: text-embedding-ada-002
- Token Usage Tracked: Yes
- Cost Tracking: Implemented

**Pricing:**
- gpt-3.5-turbo: $0.0005 per 1K input tokens, $0.0015 per 1K output tokens
- text-embedding-ada-002: $0.0001 per 1K tokens

### 7. Error Handling Strategy

**Error Types Handled:**
- Missing or invalid API key
- Empty or short text input
- File not found
- API rate limiting or quota issues
- Network errors
- ChromaDB connection issues

**User Experience:**
- All errors are caught and displayed as friendly messages
- Progress indicators show status during PDF processing
- Logging for debugging purposes

### 8. Testing Strategy

**Unit Testing:**
- PDF loading with sample PDFs
- Text splitting with sample text
- Embedding generation and search
- Question answering

**Integration Testing:**
- Full pipeline from PDF upload to answer generation
- Multi-PDF processing
- Cost tracking validation

**Edge Cases:**
- Empty PDFs
- Very large PDFs
- PDFs with no text
- Question with no relevant chunks

### 9. Security Considerations

- API keys stored in `.env` file (not in version control)
- `.gitignore` prevents sensitive files from being committed
- File uploads are limited in size
- Input validation for all user-provided values

### 10. Cost Management

- Token counting and cost tracking
- Default to gpt-3.5-turbo (less expensive)
- Number of retrieved chunks limited (5 per query)
- Option to clear collection and restart

### 11. Future Improvements

- Support for more file formats (DOCX, TXT)
- More sophisticated chunking strategies
- Better UI with rich formatting
- Deployment to cloud (AWS, Azure, or Streamlit Cloud)
- Integration with more LLMs
- Advanced filtering and metadata search

### 12. Lessons Learned

[Add 2-3 lessons learned from building this project]

### 13. Performance Metrics

| Metric | Value |
|--------|-------|
| PDF processing speed | ~2 pages/second |
| Chunk size | 500 characters |
| Chunk overlap | 50 characters |
| Number of chunks retrieved per query | 5 |
| Average response time | 2-5 seconds |
| Cost per query | ~$0.001-$0.005 |

### 14. Conclusion

The AI Research Assistant successfully demonstrates the core RAG pipeline: document ingestion, vector embedding, semantic search, and LLM-powered question answering. The system is modular, extensible, and ready for future improvements