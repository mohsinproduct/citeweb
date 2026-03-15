# File: services/audit_service.py
import random
from modules.memory.vector_store import CitewebMemory
from agents.teacher_agent import TeacherAgent
from agents.student_agent import StudentAgent
from agents.judge_agent import JudgeAgent # <-- 1. Import our new Judge Agent

class AuditService:
    def __init__(self):
        # Initialize our local memory (CPU-bound)
        self.memory = CitewebMemory()
        
        # Initialize our 3-Agent Loop (Cloud-bound reasoning to save RAM)
        self.teacher = TeacherAgent()
        self.student = StudentAgent(self.memory)
        self.judge = JudgeAgent() # <-- 2. Initialize the Judge

    def generate_audit_batch(self, target_url: str, batch_size: int = 3) -> list:
        """Picks random chunks from memory and runs the full Adversarial Audit loop."""
        
        # Fetch all stored vectors for this specific website
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
            # The Teacher generates a synthetic factual question based on the memory chunk
            test_case = self.teacher.generate_test_case(chunk)
            
            # Fast-Fail: If the Teacher hit an API limit or error, skip to the next chunk
            if "error" in test_case:
                challenges.append(test_case)
                continue
            
            # --- PHASE 2: THE STUDENT ---
            # Extract the Teacher's question and ground truth
            question = test_case.get('question', '')
            ground_truth = test_case.get('answer', '')
            
            # The Student uses the question to search the local CPU vector space
            retrieved_vectors = self.student.search_vector_space(question, target_url)
            
            # --- PHASE 3: THE JUDGE ---
            # The Judge evaluates if the Student's retrieved vectors prove the ground truth
            verdict = self.judge.evaluate_retrieval(
                question=question, 
                ground_truth=ground_truth, 
                retrieved_context=retrieved_vectors
            )
            
            # --- PACKAGE THE AUDIT TRAIL ---
            # We bundle all the evidence together so the UI can render the diagnostic cards
            test_case['retrieved_vectors'] = retrieved_vectors
            test_case['verdict'] = verdict # Saves our YES / NO / ERROR flag
            test_case['source_chunk'] = chunk # Save the original chunk for visual proof
            
            challenges.append(test_case)
            
        return challenges