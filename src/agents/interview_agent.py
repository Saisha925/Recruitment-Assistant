import os
from google import genai

class InterviewAgent:
    def __init__(self):
        self.cl = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.md = "gemini-3.5-flash"

    def gen_schedule_email(self, name: str, job_id: str) -> str:
        pmt = f"Write a professional interview scheduling email to {name} for the {job_id} position. Keep it concise and include a placeholder for a calendar link."
        res = self.cl.models.generate_content(
            model=self.md,
            contents=pmt
        )
        return res.text