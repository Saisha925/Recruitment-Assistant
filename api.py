import os
import json
import sqlite3
import traceback
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from auth import router as auth_router, init_users
from src.agents.resume_agent import ResumeAgent
from src.agents.match_agent import MatchAgent
from src.agents.rank_agent import RankAgent
from src.agents.interview_agent import InterviewAgent

load_dotenv()

app = FastAPI(title="AI Recruitment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(auth_router)
init_users()

ra = ResumeAgent()
ma = MatchAgent()
rka = RankAgent()
ia = InterviewAgent()

class SchedReq(BaseModel):
    cand_id: int
    name: str
    email: str
    job_id: str

@app.get("/api/jobs")
async def get_jobs():
    db = os.getenv("DATABASE_URL", "data/recruitment.db")
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT id, title FROM jobs")
        jobs = [{"id": r[0], "title": r[1]} for r in cur.fetchall()]
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
        res_json = ra.process_resume(file.file)
        res_json = res_json.replace('```json', '').replace('```', '').strip()
        res_data = json.loads(res_json)
        
        match_json = ma.eval_cand(res_json, job_id)
        match_json = match_json.replace('```json', '').replace('```', '').strip()
        match_data = json.loads(match_json)
        
        rank_json = rka.rank(job_id)
        leaderboard = json.loads(rank_json)
        
        return {
            "status": "success",
            "candidate": res_data,
            "match": match_data,
            "leaderboard": leaderboard
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/schedule")
async def schedule_interview(req: SchedReq):
    db = os.getenv("DATABASE_URL", "data/recruitment.db")
    try:
        txt = ia.gen_schedule_email(req.name, req.job_id)
        lnk = f"https://calendly.com/mock-recruitment/{req.job_id}"
        
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(
            "UPDATE candidates SET status = 'Scheduled' WHERE id = ?", 
            (req.cand_id,)
        )
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "email_body": txt,
            "invite_link": lnk
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)