# qa_engine.py
# Question answering engine for RAG

import os
from openai import OpenAI
from dotenv import load_dotenv
from embeddings_manager import EmbeddingsManager
from cost_tracker import CostTracker  # Add this import

load_dotenv()

class QAEngine:
    def __init__(self, collection_name="research_docs"):
        self.manager = EmbeddingsManager(collection_name)
        self.client = OpenAI()
        self.cost_tracker = CostTracker()  # Initialize cost tracker
        self.conversation_history = []
    
    def retrieve_context(self, query, n_results=5):
        """Retrieve relevant chunks from the vector database."""
        results = self.manager.search(query, n_results)
        return results
    
    def generate_answer(self, query, chunks):
        """Generate an answer based on retrieved chunks."""
        # Combine chunks into context
        context = "\n\n".join([c["text"] for c in chunks])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer the question based ONLY on the provided context. If the answer is not in the context, say so."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Cost tracking - ADD THIS SECTION
            if hasattr(response, 'usage'):
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens
                self.cost_tracker.log_completion(input_tokens, output_tokens)
                print(f"Cost tracked: {input_tokens} input, {output_tokens} output tokens")
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def ask(self, query, n_results=5, include_sources=False):
        """Ask a question and get an answer with better error handling."""
        try:
            # Check if collection is empty
            stats = self.manager.get_collection_stats()
            if stats.get("document_count", 0) == 0:
                return {
                    "answer": "No documents are loaded. Please upload a PDF first.",
                    "sources": []
                }

            # Retrieve relevant chunks
            chunks = self.retrieve_context(query, n_results)

            if not chunks:
                return {
                    "answer": "I couldn't find relevant information to answer that question. Try rephrasing or uploading more documents.",
                    "sources": []
                }

            # Generate answer
            answer = self.generate_answer(query, chunks)

            # Store conversation history
            self.conversation_history.append({
                "question": query,
                "answer": answer
            })

            result = {"answer": answer}

            if include_sources:
                result["sources"] = [
                    {"text": chunk["text"][:200] + "...", "score": chunk.get("score")}
                    for chunk in chunks[:3]
                ]

            return result

        except Exception as e:
            return {
                "answer": f"An error occurred: {str(e)}",
                "sources": []
            }
    
    def get_conversation_history(self):
        """Return the conversation history."""
        return self.conversation_history
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.")
    
    def get_cost_summary(self):
        """Get total cost summary."""
        return self.cost_tracker.get_summary()