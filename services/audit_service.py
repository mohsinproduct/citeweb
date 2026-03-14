# File: services/audit_service.py
import random
from modules.memory.vector_store import CitewebMemory
from agents.teacher_agent import TeacherAgent
from agents.student_agent import StudentAgent

class AuditService:
    def __init__(self):
        self.memory = CitewebMemory()
        self.teacher = TeacherAgent()
        self.student = StudentAgent(self.memory) # Initialize the Student with memory access

    def generate_audit_batch(self, target_url: str, batch_size: int = 3) -> list:
        """Picks random chunks from memory and asks the Teacher to create a test batch."""
        all_data = self.memory.collection.get(
            where={"source": target_url}
        )
        documents = all_data.get('documents', [])
        
        if not documents:
            return [{"error": "Memory is empty. Please audit a website first."}]

        # Ensure we don't try to pick more chunks than we actually have
        sample_size = min(batch_size, len(documents))
        target_chunks = random.sample(documents, sample_size)
        
        challenges = []
        for chunk in target_chunks:
            # --- PHASE 1: THE TEACHER ---
            test_case = self.teacher.generate_test_case(chunk)
            
            # --- PHASE 2: THE STUDENT ---
            # The Student uses the question to search the vector space
            question = test_case.get('question', '')
            retrieved_vectors = self.student.search_vector_space(question, target_url)
            
            # Package it all together
            test_case['retrieved_vectors'] = retrieved_vectors
            test_case['source_chunk'] = chunk # Save the chunk so we can show the user
            challenges.append(test_case)
            
        return challenges