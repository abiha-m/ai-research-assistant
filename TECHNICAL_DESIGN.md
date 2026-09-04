# Technical Design Document

## AI Research Assistant

## 1. System Overview

The AI Research Assistant is a Retrieval-Augmented Generation (RAG) application designed to answer questions using information contained in user-provided PDF documents.

The system combines document processing, vector embeddings, semantic retrieval, and large language model generation.

Instead of sending a user's question directly to a language model, the application first retrieves relevant information from the uploaded documents. The retrieved content is then included as context when generating the answer.

The primary system goals are:

- Process PDF documents into searchable content
- Preserve source metadata during processing
- Generate vector representations of document chunks
- Store and retrieve vectors using ChromaDB
- Retrieve relevant context using semantic similarity
- Generate answers using retrieved document context
- Provide a browser-based interface with Streamlit
- Track API usage and estimated cost

---

## 2. Current Scope

### Implemented

The current system includes:

- PDF document ingestion
- Text extraction
- Text chunking with overlap
- OpenAI embedding generation
- ChromaDB vector storage
- Semantic similarity search
- Context retrieval
- LLM-based question answering
- Multi-PDF processing
- Source metadata
- Streamlit user interface
- Conversation history
- Progress indicators
- API usage and cost tracking
- Environment-based API credential management

### Future Work

The following capabilities are not part of the current implementation and are considered future improvements:

- Additional document formats
- Advanced semantic chunking
- Automated retrieval evaluation
- User authentication
- Persistent user research sessions
- Advanced metadata filtering
- Support for additional model providers
- Production cloud deployment

---

## 3. High-Level Architecture

```text
                         User
                          |
                          v
                   Streamlit UI
                     rag_app.py
                          |
             +------------+------------+
             |                         |
             v                         v
       PDF Documents              User Question
             |                         |
             v                         |
      PDF Processor                    |
     pdf_processor.py                  |
             |                         |
             v                         |
        Text Chunks                    |
             |                         |
             v                         |
    Embeddings Manager                 |
 embeddings_manager.py                 |
             |                         |
             v                         v
          ChromaDB <------------ Query Embedding
             |
             v
       Semantic Search
             |
             v
      Relevant Chunks
             |
             v
         QA Engine
       qa_engine.py
             |
             v
        LLM Request
             |
             v
           Answer
```

---

## 4. RAG Pipeline

The application contains two primary workflows:

1. Document ingestion
2. Question answering

### 4.1 Document Ingestion

```text
PDF Upload
    |
    v
PDF Loading
    |
    v
Text Extraction
    |
    v
Text Chunking
    |
    v
Metadata Assignment
    |
    v
Embedding Generation
    |
    v
ChromaDB Storage
```

### 4.2 Question Answering

```text
User Question
      |
      v
Generate Query Embedding
      |
      v
Semantic Search
      |
      v
Retrieve Relevant Chunks
      |
      v
Construct Context
      |
      v
Build LLM Prompt
      |
      v
Generate Answer
      |
      v
Display Result
```

---

## 5. Component Design

## 5.1 PDF Processor

**File:** `pdf_processor.py`

### Responsibility

The PDF processor converts uploaded PDF documents into text that can be used by the retrieval pipeline.

### Primary Responsibilities

- Load PDF documents
- Extract text from pages
- Divide extracted text into chunks
- Preserve source information
- Preserve page metadata

### Key Operations

The component provides functionality for operations such as:

```text
load_pdf()
extract_text_from_pdf()
split_text_into_chunks()
split_documents_into_chunks()
```

### Chunking Strategy

The current implementation uses overlapping text chunks.

The existing design uses approximately:

```text
Chunk size: 500 characters
Chunk overlap: 50 characters
```

Overlap helps preserve information that may otherwise be separated at chunk boundaries.

---

## 5.2 Embeddings Manager

**File:** `embeddings_manager.py`

### Responsibility

The embeddings manager connects text content with the vector database.

Its responsibilities include:

- Generating vector embeddings
- Adding document chunks to ChromaDB
- Storing metadata
- Performing semantic searches
- Reporting collection information
- Clearing stored document collections when requested

### Conceptual Storage Model

Each stored item contains information similar to:

```text
Document Chunk
    |
    +-- Text
    |
    +-- Vector Embedding
    |
    +-- Source Metadata
    |
    +-- Unique Identifier
```

The vector representation allows document chunks to be compared semantically with user questions.

---

## 5.3 ChromaDB

### Responsibility

ChromaDB serves as the vector storage and retrieval layer.

The database stores:

- Document chunks
- Embeddings
- Metadata
- Identifiers

Conceptually:

```text
research_docs

documents  -> chunk text
embeddings -> vector representation
metadata   -> source and page information
ids        -> unique chunk identifiers
```

ChromaDB enables similarity search between a user's query embedding and previously stored document embeddings.

---

## 5.4 QA Engine

**File:** `qa_engine.py`

### Responsibility

The QA engine connects retrieval with language-model generation.

Its primary responsibilities include:

- Accepting a user question
- Retrieving relevant document chunks
- Combining retrieved chunks into context
- Constructing the model request
- Generating an answer
- Returning answer and source information

### Conceptual Flow

```text
ask(question)
     |
     v
retrieve_context(question)
     |
     v
Relevant Chunks
     |
     v
generate_answer(question, context)
     |
     v
LLM
     |
     v
Answer
```

This component represents the central connection between the retrieval and generation portions of the RAG architecture.

---

## 5.5 RAG Pipeline

**File:** `rag_pipeline.py`

### Responsibility

The RAG pipeline coordinates document ingestion operations.

It provides a higher-level layer for connecting:

```text
PDF Processing
      +
Embedding Generation
      +
Vector Storage
```

The pipeline supports processing individual documents as well as multiple PDF documents.

Separating orchestration from lower-level components keeps individual modules focused on specific responsibilities.

---

## 5.6 Streamlit Interface

**File:** `rag_app.py`

### Responsibility

The Streamlit application provides the user-facing interface.

The interface supports:

- PDF upload
- Document processing
- Question input
- Chat-style interaction
- Conversation history
- Processing status
- API usage information
- Collection management

### UI Flow

```text
Upload Documents
       |
       v
Process Documents
       |
       v
Processing Status
       |
       v
Ask Question
       |
       v
Display Answer
       |
       v
Continue Conversation
```

Streamlit session state is used where appropriate to preserve information during the active application session.

---

## 5.7 Cost Tracker

**File:** `cost_tracker.py`

### Responsibility

The cost tracker provides visibility into API usage.

The component records information related to AI operations and estimates their associated cost.

Cost tracking is useful during development because a RAG system can generate API usage during both:

1. Document embedding
2. Question answering

The purpose of this component is observability rather than billing.

Actual provider pricing can change over time, so current pricing should be verified directly with the API provider rather than treated as a fixed property of the architecture.

---

## 6. Document Processing Design

Document processing is a critical part of the retrieval system.

### Step 1: Load

The PDF is loaded and its text content is extracted.

### Step 2: Split

Extracted text is divided into smaller sections.

### Step 3: Overlap

Adjacent chunks contain overlapping text to reduce context loss at chunk boundaries.

### Step 4: Attach Metadata

Information about the source document and page is associated with chunks.

### Step 5: Embed

Each chunk is converted into a vector representation.

### Step 6: Store

The chunk, embedding, and metadata are stored in ChromaDB.

---

## 7. Retrieval Design

When a question is submitted, the system performs semantic retrieval.

```text
Question
   |
   v
Query Embedding
   |
   v
Vector Similarity Search
   |
   v
Ranked Document Chunks
   |
   v
Top Relevant Chunks
```

The current design limits the number of retrieved chunks so the model receives useful context without unnecessarily expanding the prompt.

The existing implementation is designed around retrieving approximately five relevant chunks per query.

---

## 8. Context Construction

Retrieved chunks are combined into a context block for the language model.

Conceptually:

```text
SYSTEM INSTRUCTIONS

DOCUMENT CONTEXT:
[Retrieved Chunk 1]

[Retrieved Chunk 2]

[Retrieved Chunk 3]

...

USER QUESTION:
[Question]
```

The model can then generate an answer using the retrieved document information.

This is the core distinction between the RAG architecture and a standard direct LLM request.

---

## 9. Metadata Design

Metadata provides traceability between retrieved information and its original document.

Stored metadata can include information such as:

```text
{
    "source": "document_name.pdf",
    "page": 4
}
```

Maintaining metadata enables the application to associate retrieved information with its source.

This is particularly important for research-oriented applications where users may need to verify generated answers against the original material.

---

## 10. Multi-Document Processing

The application supports processing multiple PDF documents into the retrieval collection.

Conceptually:

```text
PDF A --+
        |
PDF B --+--> Processing --> Embeddings --> ChromaDB
        |
PDF C --+
```

A user question can then retrieve relevant chunks from the processed collection.

Source metadata helps distinguish which document produced each retrieved result.

---

## 11. API Integration

The application uses external AI APIs for two primary operations:

### Embedding Generation

Text chunks and user queries are converted into vector representations.

### Answer Generation

Retrieved context and the user's question are supplied to a language model.

Model names and provider pricing are implementation details that may change over time.

For this reason, they should be configured separately from the conceptual architecture where possible.

---

## 12. Error Handling Strategy

The application must handle failures across several layers.

### Document Errors

Examples:

- Invalid PDF
- Missing file
- Empty document
- PDF with insufficient extractable text

### Configuration Errors

Examples:

- Missing API key
- Invalid environment configuration

### API Errors

Examples:

- Request failure
- Rate limiting
- Quota limitations
- Network problems

### Retrieval Errors

Examples:

- Empty vector collection
- No useful retrieved context
- Vector database failure

### UI Handling

Errors should be converted into understandable user-facing messages rather than exposing unnecessary internal details.

Logging can be used separately for debugging.

---

## 13. Security Considerations

### API Credentials

API credentials should be stored in environment variables.

Example:

```text
OPENAI_API_KEY=...
```

The `.env` file must remain excluded from version control.

### Uploaded Documents

Uploaded research documents may contain sensitive information.

The current application is a portfolio prototype and should not be treated as a secure production document-management system.

### Repository Security

Sensitive runtime data should not be committed to GitHub.

Examples include:

```text
.env
API credentials
temporary uploads
runtime logs containing sensitive data
local database files where appropriate
```

---

## 14. Cost Management

RAG systems can create API usage at multiple stages.

### Document Processing Cost

A document may be divided into many chunks, with each chunk requiring embedding generation.

### Query Cost

A question may require:

1. Query embedding
2. Retrieval
3. LLM generation

### Design Considerations

Cost can be influenced by:

- Document size
- Chunk size
- Number of chunks
- Number of retrieved chunks
- Prompt size
- Model configuration
- Number of user questions

The cost tracker provides visibility into these operations during development.

---

## 15. Testing Strategy

Testing should cover individual components and the complete RAG workflow.

### Component Testing

Important areas include:

- PDF loading
- Text extraction
- Chunk creation
- Metadata preservation
- Embedding generation
- Vector storage
- Semantic search
- Context retrieval
- Answer generation
- Cost tracking

### Integration Testing

The complete workflow should also be tested:

```text
PDF
 |
 v
Process
 |
 v
Store
 |
 v
Ask Question
 |
 v
Retrieve
 |
 v
Generate
 |
 v
Answer
```

### Edge Cases

Useful edge cases include:

- Empty PDFs
- PDFs with little extractable text
- Large documents
- Multiple documents
- Empty collection
- Questions with weak retrieval matches
- API failures

---

## 16. Repository Structure

The project is organized around separate responsibilities:

```text
ai-research-assistant/
|
├── rag_app.py
├── rag_pipeline.py
├── qa_engine.py
├── embeddings_manager.py
├── pdf_processor.py
├── cost_tracker.py
├── requirements.txt
├── README.md
├── TECHNICAL_DESIGN.md
├── reflections.md
└── .gitignore
```

This modular structure separates document processing, retrieval, generation, orchestration, tracking, and presentation.

---

## 17. Technology Stack

| Technology | Role |
|---|---|
| Python | Application development |
| Streamlit | User interface |
| OpenAI API | Embeddings and generation |
| ChromaDB | Vector storage and retrieval |
| LangChain | Document-processing utilities |
| PyPDFLoader | PDF extraction |
| python-dotenv | Environment configuration |
| Git | Version control |
| GitHub | Repository hosting |

---

## 18. Key Design Decisions

### Modular Components

Document processing, retrieval, generation, cost tracking, and UI logic are separated into different modules.

This improves maintainability and makes individual parts easier to test.

### Overlapping Chunks

Chunk overlap helps reduce context loss when relevant information crosses a chunk boundary.

### Vector Retrieval

Semantic retrieval allows information to be found based on meaning rather than exact keyword matches.

### Metadata Preservation

Source metadata is maintained so retrieved information can be associated with the original document.

### Limited Context Retrieval

Only a limited number of highly relevant chunks are supplied to the model.

This helps control prompt size while attempting to preserve useful context.

---

## 19. Current Limitations

The current architecture has several limitations.

### Retrieval Evaluation

The project does not currently include a formal benchmark for measuring retrieval quality.

### Fixed Chunking

A fixed-size chunking strategy may not align with the semantic structure of every document.

### Model Dependency

The application depends on external AI services for embeddings and answer generation.

### Limited Document Types

The ingestion pipeline primarily targets PDF documents.

### Generated Answers

RAG can improve grounding but does not guarantee that every generated statement is correct.

Important information should still be verified against the original documents.

### Production Readiness

The project is designed as a portfolio prototype rather than a production document-management system.

---

## 20. Future Architecture

A more advanced version could expand the architecture to:

```text
                  User
                   |
                   v
              Web Interface
                   |
          +--------+--------+
          |                 |
          v                 v
   Document Manager     Query Manager
          |                 |
          v                 v
   Parsing Pipeline    Query Processing
          |                 |
          v                 |
 Semantic Chunking          |
          |                 |
          v                 v
       Embeddings ------> Retrieval
          |                 |
          v                 v
      Vector DB ------> Reranking
                            |
                            v
                     Context Builder
                            |
                            v
                       LLM Layer
                            |
                            v
                  Answer + Citations
                            |
                            v
                     RAG Evaluation
```

This could support more sophisticated retrieval, evaluation, and source presentation.

---

## 21. Future Improvements

Potential improvements include:

- Additional document formats
- Semantic chunking
- Structure-aware document parsing
- Retrieval reranking
- Automated retrieval evaluation
- Automated answer evaluation
- Improved metadata filtering
- Better source visualization
- Additional embedding models
- Additional LLM providers
- Persistent user sessions
- User authentication
- Cloud deployment
- Improved large-document handling

---

## 22. Engineering Lessons

The project demonstrated several important principles.

### Retrieval Quality Matters

A capable language model cannot compensate for consistently poor retrieval.

### Document Processing Is Part of AI System Design

Chunking and metadata decisions directly affect downstream retrieval.

### RAG Is a Pipeline

The application is not simply an LLM with a PDF attached.

It consists of multiple stages that must work together.

### Observability Matters

Tracking errors, progress, and API usage makes the system easier to understand and debug.

### Source Traceability Matters

For research applications, users should be able to connect retrieved information back to its original source.

---

## 23. Project Status

**Status: Functional RAG Prototype**

Implemented:

- PDF processing
- Text chunking
- Vector embeddings
- ChromaDB storage
- Semantic retrieval
- Context construction
- LLM answer generation
- Multi-PDF processing
- Source metadata
- Streamlit interface
- Conversation history
- Progress indicators
- API usage and cost tracking

Planned:

- Advanced chunking
- Retrieval evaluation
- Additional document formats
- Advanced metadata filtering
- Persistent user sessions
- Authentication
- Production deployment

---

## 24. Author

**Abiha Majid**

Engineering Student  
Northern Virginia Community College

---

## 25. Related Project

**AI Engineering Tutor**

An AI application designed to generate structured explanations of engineering concepts.

Repository:

https://github.com/abiha-m/ai-engineering-tutor

---

## 26. Documentation

- `README.md` - Project overview and setup instructions
- `TECHNICAL_DESIGN.md` - Architecture and engineering decisions
- `reflections.md` - Development experience and lessons learned

---

## 27. Version

Current version: Functional portfolio prototype
