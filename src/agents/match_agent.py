import json
from src.schemas import JobDesc, MatchResult, ResumeData

SYS_PROMPT = """
You are the Job Matching Agent.
Compare the provided candidate ResumeData against the target JobDesc.
Calculate a match score from 0.0 to 100.0 based on skill overlap and minimum experience.
Output MUST strictly follow the MatchResult JSON schema.
Status must be either 'Shortlisted' or 'Rejected' (threshold: 75.0).
"""

class MatchAgent:
    def __init__(self, llm=None, mcp=None):
        self.llm = llm
        self.mcp = mcp
        self.sys_prompt = SYS_PROMPT

    def get_job(self, job_id: str) -> str:
        mock_job = {
            "id": job_id,
            "title": "AI/ML Engineer",
            "req_skills": ["Python", "C++", "Machine Learning"],
            "min_yoe": 2.0
        }
        return json.dumps(mock_job)

    def eval_cand(self, res_json: str, job_id: str) -> str:
        cand = ResumeData.model_validate_json(res_json)
        job = JobDesc.model_validate_json(self.get_job(job_id))
        
        # Simulated LLM inference mapping to MatchResult
        score = 80.0 
        reason = "Meets minimum YOE. Strong Python skills, but lacks explicit C++ and ML mentions."
        status = "Shortlisted"

        res = MatchResult(
            cand_id=cand.email,
            job_id=job.id,
            score=score,
            reason=reason,
            status=status
        )
        return res.model_dump_json(indent=4)

if __name__ == "__main__":
    agent = MatchAgent()
    
    test_res = '''{
        "name": "John Doe",
        "email": "john.doe@email.com",
        "skills": ["Python", "SQL", "Software Engineering"],
        "edu": "B.Tech",
        "yoe": 3.5
    }'''
    
    final_json = agent.eval_cand(test_res, "REQ-101")
    print(final_json)