import json
from src.agents.resume_agent import ResumeAgent
from src.agents.match_agent import MatchAgent
from src.agents.rank_agent import RankAgent
from src.agents.interview_agent import InterviewAgent

class RecruitmentOrchestrator:
    def __init__(self):
        print("[System] Initializing AI Agents...")
        self.resume_agent = ResumeAgent()
        self.match_agent = MatchAgent()
        self.rank_agent = RankAgent()
        self.interview_agent = InterviewAgent()

    def process_new_applicant(self, file_path: str, job_id: str):
        print(f"\n{'='*55}")
        print(f"🚀 NEW APPLICANT WORKFLOW TRIGGERED")
        print(f"{'='*55}")

        # Step 1: Parse Resume
        print("\n[Step 1] Parsing Resume Document...")
        resume_json = self.resume_agent.process_resume(file_path)
        
        # Step 2: Match Candidate to Job
        print(f"\n[Step 2] Evaluating candidate against Job ID: {job_id}...")
        match_result_json = self.match_agent.eval_cand(resume_json, job_id)
        match_result = json.loads(match_result_json)
        
        cand_id = match_result.get("cand_id")
        status = match_result.get("status")
        score = match_result.get("score")
        
        print(f"   -> Result: {status} (Score: {score})")
        print(f"   -> Justification: {match_result.get('reason')}")

        # Step 3: Update Leaderboard
        print(f"\n[Step 3] Updating Candidate Leaderboard...")
        # In a real app, the MatchAgent saves to the DB, and RankAgent reads from it.
        # We trigger the rank agent here to simulate the leaderboard refresh.
        self.rank_agent.rank(job_id)
        print("   -> Leaderboard successfully updated.")

        # Step 4: Conditional Interview Scheduling
        if status == "Shortlisted":
            print(f"\n[Step 4] Candidate Shortlisted! Coordinating Interview...")
            booking_json = self.interview_agent.book(cand_id)
            booking_data = json.loads(booking_json)
            print(f"   -> ✅ SUCCESS: Interview booked for {cand_id}")
            print(f"   -> 📅 Time: {booking_data.get('start')} to {booking_data.get('end')}")
        else:
            print(f"\n[Step 4] Candidate Rejected. Halting workflow.")

        print(f"\n{'='*55}")
        print(f"🏁 WORKFLOW COMPLETE")
        print(f"{'='*55}\n")

if __name__ == "__main__":
    orchestrator = RecruitmentOrchestrator()
    
    # Simulate a new application arriving in the Applicant Tracking System
    test_resume_path = "C:/resumes/john_doe_resume.pdf"
    target_job_req = "REQ-101"
    
    orchestrator.process_new_applicant(test_resume_path, target_job_req)