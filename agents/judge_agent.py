# File: agents/judge_agent.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class JudgeAgent:
    def __init__(self):
        # TEMPERATURE = 0.0 for deterministic grading.
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.0 
        )

    def evaluate_retrieval(self, question: str, ground_truth: str, retrieved_context: list) -> str:
        """
        Evaluates if the local Student Agent retrieved enough factual signal 
        to accurately answer the Teacher's question.
        Returns: 'YES', 'NO', or 'ERROR'
        """
        # Fast-Fail: If the Student found absolutely nothing in our local ChromaDB, 
        # immediately fail it.
        if not retrieved_context:
            return "NO"

        
        context_str = "\n---\n".join(retrieved_context)

        
        system_prompt = (
            "You are the 'Judge Agent' for an AI citation auditor.\n"
            "Your job is to strictly evaluate if the provided 'Retrieved Context' contains enough factual evidence to answer the 'Question'.\n"
            "The context MUST mathematically align with the 'Ground Truth'.\n"
            "If the context proves the answer, output strictly: [YES]\n"
            "If the context is irrelevant, missing, or lacks factual density, output strictly: [NO]\n"
            "Do not output any other text. No explanations."
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", f"Question: {question}\nGround Truth: {ground_truth}\nRetrieved Context:\n{context_str}")
        ])

        try:
            chain = prompt | self.llm
            response = chain.invoke({})
            content = response.content.strip().upper()
            
            
            if "YES" in content:
                return "YES"
            return "NO"
            
        except Exception as e:
            print(f"Judge Agent API Error: {e}")
            return "ERROR"