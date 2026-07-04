## Week 1 Summary 

### What I Built
- Complete text summarizer application with menu interface
- Batch processing for multiple files
- Logging system for all operations
- Professional README and design documentation

### Skills I Learned
- Python programming (functions, error handling, file I/O)
- OpenAI API integration
- Git and GitHub (add, commit, push, status)
- Virtual environments
- Environment variables (.env)
- Logging and debugging
- Documentation and presentation

### Certifications Earned
- ChatGPT Prompt Engineering for Developers (DeepLearning.AI)

### Challenges I Faced
- Understanding how to structure the menu interface
- Fixing encoding errors when reading log files
- Learning the Git workflow (add, commit, push)

### How I Solved Them
- Broke the menu into separate functions for each option
- Added `errors='ignore'` parameter to file reading
- Practiced the Git cycle repeatedly until it became natural

### What I Learned About Myself
- I can build real applications even when I feel unsure
- I learn best by doing and fixing errors as they come

### One Sentence Summary of Week 1
I built a complete AI-powered text summarizer application from scratch using Python and the OpenAI API.

### Day 8 

**What I learned today:**
- How to load and extract text from PDFs using PyPDFLoader
- How to split text into overlapping chunks
- How to handle different PDF structures
- How to extract metadata from PDFs

**What was difficult:**
- [Write one sentence about something challenging]

**How I solved it:**
- [Write one sentence about how you solved it]

**What I will do tomorrow:**
- Generate embeddings for chunks
- Store embeddings in memory
- Set up Chroma vector database

### Day 9 

**What I learned today:**
- How to generate embeddings using OpenAI's text-embedding-ada-002
- How to set up ChromaDB as a persistent vector database
- How to add documents to a collection
- How to perform similarity searches
- How to integrate PDF processing with embeddings

**What was difficult:**
- Understanding how ChromaDB stores and retrieves embeddings
- Figuring out the metadata format required for ChromaDB

**How I solved it:**
- Read the ChromaDB documentation and tested with small examples
- Added proper metadata to each chunk before storing

**What I will do tomorrow:**
- Build the question-answering component
- Connect retrieval with GPT

### Day 10 

**What I learned today:**
- How to build a question-answering system using RAG
- How to integrate retrieval with GPT
- How to build a Streamlit UI
- How to manage conversation history

**What was difficult:**
- Understanding how to connect all the components together
- Making the Streamlit interface user-friendly

**How I solved it:**
- Broke down the problem into smaller steps and tested each one
- Used Streamlit's built-in components for a clean interface

**What I will do tomorrow:**
- Polish the Streamlit UI
- Add error handling
- Test with multiple PDFs

### Day 11 

**What I learned today:**
- How to support multiple PDFs in one collection
- How to implement cost tracking for API calls
- How to add progress indicators in Streamlit
- How to handle edge cases and errors gracefully

**What was difficult:**
- [Write one sentence about something challenging]

**How I solved it:**
- [Write one sentence about how you solved it]

**What I will do tomorrow:**
- Write a complete technical design document
- Prepare final demos
## Week 2 

### What I Built:
- Complete AI Research Assistant (RAG) system
- PDF processing pipeline with text extraction
- Embeddings and vector storage with ChromaDB
- Question answering with GPT-3.5-turbo
- Streamlit web interface with progress indicators
- Multi-PDF support
- Cost tracking for API usage
- Complete technical documentation (DESIGN.md)

### Skills I Learned:
- PDF extraction with LangChain PyPDFLoader
- Text chunking with overlap strategy
- OpenAI embeddings (text-embedding-ada-002)
- Vector databases (ChromaDB)
- Semantic search
- Retrieval-Augmented Generation (RAG)
- Streamlit UI development
- API cost tracking

### Certifications Working On:
- LangChain for LLM Applications (DeepLearning.AI) - In progress

### Challenges I Faced:
1. Fixing encoding errors when reading PDFs
2. Understanding how to optimize chunk size for retrieval
3. Debugging the ChromaDB metadata issue
4. Making the Streamlit progress bar work correctly

### How I Solved Them:
1. Added proper error handling with try/except blocks
2. Tested different chunk sizes (500 chars, 50 overlap)
3. Added metadata with proper formatting for each chunk
4. Used Streamlit's status and progress bar components correctly

### What I Learned About Myself:
- I can build complex AI systems by breaking them down into smaller components
- I enjoy the challenge of debugging and solving technical problems
- I'm capable of learning new technologies quickly when building real projects

### Three Sentences for Essays:
1. I built a complete RAG system that can ingest PDFs and answer user questions using advanced AI techniques.
2. The most difficult part was optimizing chunk sizes and retrieval parameters to get accurate responses.
3. I learned that building production-ready AI systems requires attention to detail, error handling, and user experience.

Final Review

#### What I Built
- Complete RAG system with PDF processing, embeddings, vector search, and question answering
- Streamlit UI for easy interaction
- Multi-PDF support
- Cost tracking system
- Progress indicators for better user experience

#### Skills Learned
- RAG architecture
- Vector databases (ChromaDB)
- Embeddings (OpenAI text-embedding-ada-002)
- Semantic search
- LLM integration (GPT-3.5-turbo)
- Streamlit web development
- Cost tracking for API usage
- PDF processing with LangChain

#### Certifications Earned
- LangChain for LLM Applications (DeepLearning.AI) - Complete
- ChatGPT Prompt Engineering for Developers (DeepLearning.AI) - Complete
- Git & GitHub (freeCodeCamp) - Complete

#### Challenges Faced
- Understanding how to structure the RAG pipeline end-to-end
- Fixing ChromaDB metadata errors when adding chunks
- Debugging the Streamlit progress bar implementation
- Handling large PDFs efficiently

#### How I Solved Them
- Broke the pipeline into smaller components and tested each one
- Added proper metadata formatting for each chunk
- Used Streamlit's status and progress components correctly
- Optimized chunk size to 500 characters with 50 overlap

#### What I Learned About Myself
- I can learn new technologies quickly when I have a real project to build
- I enjoy solving problems and debugging code

#### What I Will Do Differently in Project 2
- Plan the architecture more carefully before writing code
- Add more error handling from the start

#### Final Thoughts on Project 1
This project taught me how to build a complete AI application from scratch. I learned how PDF processing, embeddings, vector databases, and LLMs work together to create a powerful RAG system. The most valuable lesson was that building systems that work end-to-end is more important than perfect code. I'm proud of what I built in two weeks.

#### Three Sentences for My Application Essay
1. I built a complete AI research assistant that can read and understand PDFs.
2. The hardest part was integrating the vector database with the LLM for accurate retrieval.
3. I learned that building systems that work end-to-end is more important than perfect code.