import os
import json
import sqlite3
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.schemas import JobDesc, MatchResult, ResumeData
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

# We tweaked the prompt to ensure it counts your academic/internship work!
SYS_PROMPT = """
You are the Job Matching Agent.
Compare ResumeData against JobDesc.
Calculate match score (0.0 to 100.0). 
CRITICAL: You must count rigorous academic projects and internships as valid Years of Experience (YOE).
Output MatchResult JSON schema. Status must be 'Shortlisted' or 'Rejected' (threshold: 75.0).
"""

class MatchAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.db_path = os.getenv("DATABASE_URL", "data/recruitment.db")

    def get_job(self, j_id: str) -> str:
        conn = sqlite3.connect(self.db_path)
        curr = conn.cursor()
        curr.execute("SELECT title, skills, min_yoe FROM jobs WHERE id = ?", (j_id,))
        row = curr.fetchone()
        conn.close()
        
        if row:
            job = {"id": j_id, "title": row[0], "req_skills": json.loads(row[1]), "min_yoe": row[2]}
            return json.dumps(job)
        return json.dumps({"error": "Job not found"})

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
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
        
        # 1. Parse the AI's decision
        match_data = MatchResult.model_validate_json(res.text)
        
        # 2. Save the AI's decision to the SQLite Database so the RankAgent can see it!
        conn = sqlite3.connect(self.db_path)
        curr = conn.cursor()
        curr.execute("""
            INSERT OR REPLACE INTO candidates (id, score, reason, status)
            VALUES (?, ?, ?, ?)
        """, (match_data.cand_id, match_data.score, match_data.reason, match_data.status))
        conn.commit()
        conn.close()
        
        return res.text