import json

SYS_PROMPT = """
You are the Interview Coordination Agent.
Take a shortlisted candidate email, find available interview slots, and book the earliest one.
Output a JSON object strictly containing 'status', 'cand_id', 'start', and 'end'.
"""

class InterviewAgent:
    def __init__(self, llm=None, mcp=None):
        self.llm = llm
        self.mcp = mcp
        self.prompt = SYS_PROMPT

    def get_slots(self, email: str) -> str:
        mock = {"available_slots": ["2026-06-05T10:00:00", "2026-06-05T14:00:00", "2026-06-06T11:00:00"]}
        return json.dumps(mock)

    def book(self, cand_id: str) -> str:
        raw = self.get_slots("recruiter@company.com")
        slots = json.loads(raw)["available_slots"]
        
        start = slots[0]
        end = start.replace("10:00", "11:00") 
        
        res = {
            "status": "booked",
            "cand_id": cand_id,
            "start": start,
            "end": end
        }
        return json.dumps(res, indent=4)

if __name__ == "__main__":
    agent = InterviewAgent()
    out = agent.book("john.doe@email.com")
    print(out)