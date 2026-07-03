# Technical Design Document: AI Research Assistant

## 1. Overview

This document describes the technical design of the AI Research Assistant project, built as part of an AI engineering portfolio. The project consists of two main components:

1. **Text Summarizer** (Week 1) - A command-line application for summarizing text from files and direct input.
2. **RAG System** (Week 2) - A Retrieval-Augmented Generation system for answering questions from PDF documents.

---

## 2. Architecture

### High-Level Architecture
┌─────────────────────────────────────────────────────────────────┐
│ AI Research Assistant │
├─────────────────────────────┬───────────────────────────────────┤
│ Week 1: Summarizer │ Week 2: RAG System │
├─────────────────────────────┼───────────────────────────────────┤
│ • Menu Interface (app.py) │ • PDF Processor │
│ • Core Summarizer │ • Embeddings Manager │
│ • Batch Processor │ • QA Engine │
│ • Logging System │ • Streamlit UI │
│ │ • Cost Tracker │
└─────────────────────────────┴───────────────────────────────────┘

### Component Details

#### Week 1: Text Summarizer

1. **Menu Interface** (`app.py`)
   - Handles user interaction
   - Displays menu options (1-6)
   - Routes user requests to appropriate functions

2. **Core Summarizer** (`summarizer.py`)
   - `summarize(text, max_length)`: Main summarization function using OpenAI API
   - `read_file(file_path)`: Reads text from files
   - `save_summary(text, output_path)`: Saves summaries to files
   - `log_summary(input_text, output_text)`: Logs operations

3. **Batch Processor** (`batch_summarizer.py`)
   - Processes all .txt files in a folder
   - Handles errors per file
   - Creates output summaries

4. **Interactive Version** (`interactive_summarizer.py`)
   - Allows users to test summarization interactively
   - Includes logging for each summary

#### Week 2: RAG System

1. **PDF Processor** (`pdf_processor.py`)
   - Loads PDFs using LangChain's PyPDFLoader
   - Extracts text from all pages
   - Splits text into overlapping chunks

2. **Embeddings Manager** (`embeddings_manager.py`)
   - Generates embeddings using OpenAI's text-embedding-ada-002
   - Manages ChromaDB vector database
   - Handles semantic search

3. **QA Engine** (`qa_engine.py`)
   - Retrieves relevant chunks from vector database
   - Generates answers using GPT-3.5-turbo
   - Tracks conversation history
   - Includes cost tracking

4. **Streamlit UI** (`rag_app.py`)
   - Web interface for users
   - PDF upload and processing
   - Chat interface for questions
   - Progress indicators
   - Cost display

5. **Cost Tracker** (`cost_tracker.py`)
   - Tracks API token usage
   - Calculates costs
   - Stores cost data in JSON format

---

### Detailed RAG Flow:
1. User uploads a PDF via Streamlit UI
2. PDF is saved to temp directory
3. PDF text is extracted page by page
4. Text is split into overlapping chunks (500 chars, 50 overlap)
5. OpenAI embeddings are generated for each chunk
6. Embeddings are stored in ChromaDB with metadata
7. User asks a question
8. Query is embedded and used to search ChromaDB
9. Top 5 most relevant chunks are retrieved
10. Chunks are combined into context
11. GPT-3.5-turbo generates an answer
12. Answer is displayed with sources

---

## 4. Error Handling Strategy

The application handles these error types:
- Missing or invalid API key
- Empty or short text input
- File not found
- Invalid PDF format
- API rate limiting or quota issues
- Network errors
- Generic exceptions

Each error is caught, logged, and displayed as a friendly message to the user.

---

## 5. API Integration

### OpenAI API
- **Provider**: OpenAI
- **Models Used**:
  - `gpt-3.5-turbo`: Text summarization and question answering
  - `text-embedding-ada-002`: Embedding generation for RAG
- **Parameters**: temperature=0.3-0.5, max_tokens=200-500

### Cost Management
- Token counting is tracked via logging
- Cost tracker stores all API usage
- Average cost per question: ~$0.001 - $0.005

---

## 6. Security Considerations

- API key is stored in `.env` file (not in version control)
- `.gitignore` prevents `.env` from being committed
- No user data is stored permanently (only logs summary operations)
- PDFs are deleted after processing

---

## 7. Testing Strategy

- Unit testing: Each function is tested independently
- Integration testing: Full workflow tested from menu to output
- Edge case testing: Empty input, very long input, malformed files
- UI testing: Streamlit app tested with multiple PDFs

---

## 8. Future Improvements

- Add support for more file formats (DOCX, HTML)
- Add caching to reduce API calls and costs
- Add user authentication
- Deploy to Streamlit Cloud or Hugging Face Spaces
- Add PDF metadata extraction
- Implement better chunking strategies

---

## 9. Lessons Learned

1. **Error handling is essential** - A robust application needs to handle all possible errors gracefully.
2. **Chunk size and overlap** significantly impact retrieval quality in RAG systems.
3. **Logging helps debugging** - Having a log file made it much easier to track issues.
4. **Progress indicators** improve user experience in web applications.
5. **Cost tracking** is important for managing API usage.
6. **Git workflow** - Learning add, commit, push was essential for tracking progress.
7. **Testing each function** independently saved time when debugging the full application.