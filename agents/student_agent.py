# File: agents/student_agent.py

class StudentAgent:
    def __init__(self, memory_service):
        # Pass the memory service so the Student can search ChromaDB directly
        self.memory = memory_service

    def search_vector_space(self, question: str, target_url: str, top_k: int = 3) -> list:
        """
        The Searcher: Performs Cosine Similarity Search to find the chunks 
        mathematically closest in meaning to the Teacher's question.
        Returns pure text chunks.
        """
        try:
            search_results = self.memory.collection.query(
                query_texts=[question],
                where={"source": target_url},
                n_results=top_k
            )
            
            # Extract and return the raw text chunks
            if search_results and search_results['documents']:
                return search_results['documents'][0]
            return []
            
        except Exception as e:
            print(f"Student Vector Search Error: {e}")
            return []