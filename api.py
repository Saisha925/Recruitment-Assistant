import os
import json
import sqlite3
import traceback # Add this at the very top of api.py with your other imports!

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.agents.resume_agent import ResumeAgent
from src.agents.match_agent import MatchAgent
from src.agents.rank_agent import RankAgent
from src.agents.interview_agent import InterviewAgent

app = FastAPI(title="AI Recruitment API")

# Allow your React app (running on a different port) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Default Next.js port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
ra = ResumeAgent()
ma = MatchAgent()
rka = RankAgent()
ia = InterviewAgent()

@app.get("/api/jobs")
async def get_jobs():
    """Fetch available jobs from the SQLite database."""
    db_path = os.getenv("DATABASE_URL", "data/recruitment.db")
    try:
        conn = sqlite3.connect(db_path)
        curr = conn.cursor()
        curr.execute("SELECT id, title FROM jobs")
        jobs = [{"id": row[0], "title": row[1]} for row in curr.fetchall()]
        conn.close()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/process-resume")
async def process_resume(
    job_id: str = Form(...),
    file: UploadFile = File(...)
    ):
    try:
        print(f"🚀 Starting pipeline for Job ID: {job_id}")
        
        # 1. Parse Resume 
        res_json = ra.process_resume(file.file)
        print("✅ Resume parsed successfully!")
        
        # Clean markdown formatting if Gemini added it
        res_json = res_json.replace('```json', '').replace('```', '').strip()
        res_data = json.loads(res_json)
        
        # 2. Match Candidate
        match_json = ma.eval_cand(res_json, job_id)
        print("✅ Candidate matched successfully!")
        
        # Clean markdown formatting here too
        match_json = match_json.replace('```json', '').replace('```', '').strip()
        match_data = json.loads(match_json)
        
        # 3. Rank Candidate
        ra_agent.rank_candidate(
            cand_id=res_data.get("email", "unknown"),
            job_id=job_id,
            score=match_data.get("score", 0),
            status=match_data.get("status", "pending")
        )
        print("✅ Candidate ranked and saved to SQLite!")
        
        # 4. Get Leaderboard
        leaderboard = ra_agent.get_leaderboard(job_id)
        
        return {
            "status": "success",
            "candidate": res_data,
            "match": match_data,
            "leaderboard": leaderboard
        }
        
    except Exception as e:
        print("\n" + "="*50)
        print("❌ PIPELINE CRASHED! Here is the exact error:")
        traceback.print_exc()  # This will force the terminal to show the exact line that failed!
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/schedule-interview")
async def schedule_interview(email: str = Form(...)):
    """Trigger the Interview Agent."""
    try:
        booking_json = ia.book(email)
        return json.loads(booking_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
    