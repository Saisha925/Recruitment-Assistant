from pydantic import BaseModel
from typing import List

class ResumeData(BaseModel):
    name: str
    email: str
    skills: List[str]
    edu: str
    yoe: float

class JobDesc(BaseModel):
    id: str
    title: str
    req_skills: List[str]
    min_yoe: float

class MatchResult(BaseModel):
    cand_id: str
    job_id: str
    score: float
    reason: str
    status: str