import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.schemas import ResumeData

load_dotenv()

SYS_PROMPT = """
You are the Resume Screening Agent.
Extract candidate name, email, skills, education, and yoe.
Output MUST perfectly match the ResumeData JSON schema.
Do NOT evaluate or rank.
"""

class ResumeAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def get_raw_text(self, f_path: str) -> str:
        return """
        Saisha Bhasin
        Email: saisha.bhasin@email.com
        Education: B.Tech in Artificial Intelligence and Machine Learning, IGDTUW
        Experience: Incoming Intern at HCLTech. 1 year of applied project experience.
        Skills: C++, Python, Machine Learning, NLP, Transformers, LLMs.
        """

    def process_resume(self, f_path: str) -> str:
        raw = self.get_raw_text(f_path)
        
        res = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Extract this raw resume data into JSON: {raw}",
            config=types.GenerateContentConfig(
                system_instruction=SYS_PROMPT,
                response_mime_type="application/json",
                response_schema=ResumeData,
                temperature=0.0
            )
        )
        return res.text

if __name__ == "__main__":
    ag = ResumeAgent()
    print(ag.process_resume("dummy_path.pdf"))