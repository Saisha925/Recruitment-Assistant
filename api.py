import os
import json
import sqlite3
from fastapi import FastAPI, UploadFile, Form, HTTPException
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
async def process_resume(file: UploadFile, job_id: str = Form(...)):
    """Run the AI Pipeline on an uploaded resume."""
    try:
        # 1. Parse Resume (Pass the raw file stream)
        res_json = ra.process_resume(file.file)
        res_data = json.loads(res_json)
        
        # 2. Match Candidate
        match_json = ma.eval_cand(res_json, job_id)
        match_data = json.loads(match_json)
        
        # 3. Update Leaderboard
        rank_json = rka.rank(job_id)
        rank_data = json.loads(rank_json)
        
        return {
            "status": "success",
            "candidate": res_data,
            "match": match_data,
            "leaderboard": rank_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"\n❌ PIPELINE CRASHED: {str(e)}\n") # <-- Add this line
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
    