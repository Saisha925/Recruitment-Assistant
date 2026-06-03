import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.schemas import JobDesc, MatchResult, ResumeData

load_dotenv()

SYS_PROMPT = """
You are the Job Matching Agent.
Compare ResumeData against JobDesc.
Calculate match score (0.0 to 100.0).
Output MatchResult JSON schema. Status must be 'Shortlisted' or 'Rejected' (threshold: 75.0).
"""

class MatchAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def get_job(self, j_id: str) -> str:
        job = {
            "id": j_id,
            "title": "Data Scientist",
            "req_skills": ["Python", "Machine Learning", "NLP", "LLMs"],
            "min_yoe": 0.5
        }
        return json.dumps(job)

    def eval_cand(self, res_json: str, j_id: str) -> str:
        job_json = self.get_job(j_id)
        prompt = f"Resume:\n{res_json}\n\nJob Requirements:\n{job_json}"
        
        res = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYS_PROMPT,
                response_mime_type="application/json",
                response_schema=MatchResult,
                temperature=0.0
            )
        )
        return res.text

if __name__ == "__main__":
    ag = MatchAgent()
    test_res = '{"name":"Saisha Bhasin","email":"saisha.bhasin@email.com","skills":["C++","Python","Machine Learning","NLP","LLMs"],"edu":"B.Tech AI/ML","yoe":1.0}'
    print(ag.eval_cand(test_res, "REQ-102"))