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