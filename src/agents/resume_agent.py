import os
import json
import PyPDF2
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.schemas import ResumeData
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()
SYS_PROMPT = """
You are the Resume Screening Agent.
Extract candidate name, email, skills, education, and yoe.

CRITICAL INSTRUCTION FOR YOE: 
Do not just look for full-time professional employment. You MUST calculate 'yoe' by aggregating the duration of all academic projects, internships, hackathons, and technical coursework. 
Rule of thumb: 1 rigorous academic year in an AI/ML program + projects/internships should equate to at least 0.5 to 1.0 YOE. Be generous.

CRITICAL INSTRUCTION FOR SKILLS: 
Thoroughly scan the entire document, including project descriptions, for advanced AI/ML terms like 'NLP', 'LLMs', 'Transformers', 'Deep Learning', and 'Natural Language Processing'. Extract them explicitly if they are mentioned anywhere.

Output MUST perfectly match the ResumeData JSON schema.
Do NOT evaluate or rank.
"""

class ResumeAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def extract_text_from_pdf(self, file_input) -> str:
        """Reads a PDF, resets the pointer, and sanitizes text."""
        text = ""
        try:
            if isinstance(file_input, str):
                with open(file_input, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
            else:
                # CRITICAL: Rewind the Streamlit file pointer to the beginning!
                file_input.seek(0) 
                reader = PyPDF2.PdfReader(file_input)
                for page in reader.pages:
                    # Some pages might return None if they are purely images
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # CRITICAL: Clean up null bytes that cause Gemini HTTP 400 errors
            return text.replace('\x00', '')
            
        except Exception as e:
            print(f"[ResumeAgent] Error extracting PDF text: {e}")
            return ""

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    def process_resume(self, file_input) -> str:
        # 1. Actually read the PDF!
        raw_text = self.extract_text_from_pdf(file_input)
        
        if not raw_text.strip():
            # Fallback if the PDF is unreadable (e.g., an image-only PDF without OCR)
            return json.dumps({
                "name": "Unknown", "email": "Unknown", "skills": [], "edu": "Unknown", "yoe": 0.0
            })
            
        print("[ResumeAgent] PDF text successfully extracted. Sending to Gemini...")
        
        # 2. Pass the real text to the LLM
        res = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Extract this raw resume data into JSON: {raw_text}",
            config=types.GenerateContentConfig(
                system_instruction=SYS_PROMPT,
                response_mime_type="application/json",
                response_schema=ResumeData,
                temperature=0.0
            )
        )
        return res.text