# File: agents/teacher_agent.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class TeacherAgent:
    def __init__(self):
        # Using Gemini 2.5 Flash for high-speed, factual reasoning
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2 # Low temp = strict, factual generation
        )

    def generate_test_case(self, context_chunk: str) -> dict:
        """Generates a synthetic question and answer based on a specific memory fragment."""
        system_prompt = (
            "You are the 'Teacher Agent' for citeweb.ai. Your job is to create "
            "a verification test based ONLY on the provided text snippet. "
            "The question must be factual and specific. "
            "Output your response strictly in the following format:\n"
            "QUESTION: [Your question]\n"
            "ANSWER: [Your ground truth answer]"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", f"Text Snippet: {context_chunk}")
        ])

        try:
            chain = prompt | self.llm
            response = chain.invoke({})
            content = response.content
            
            # Parse the strict formatting into a dictionary
            q_part = content.split("QUESTION:")[1].split("ANSWER:")[0].strip()
            a_part = content.split("ANSWER:")[1].strip()
            return {"question": q_part, "answer": a_part}
        except Exception as e:
            return {"error": f"Failed to parse Teacher's output: {str(e)}"}