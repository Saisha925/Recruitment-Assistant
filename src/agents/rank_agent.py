import json
from src.schemas import MatchResult

SYS_PROMPT = """
You are the Ranking Agent.
Take a list of candidate results and return a ranked leaderboard.
Sort by 'score' in descending order.
Output a JSON array containing 'rank', 'cand_id', 'score', and 'status'.
"""

class RankAgent:
    def __init__(self, llm=None, mcp=None):
        self.llm = llm
        self.mcp = mcp
        self.prompt = SYS_PROMPT

    def get_cands(self, j_id: str) -> str:
        mock = [
            {"cand_id": "alice@email.com", "job_id": j_id, "score": 92.5, "reason": "Excellent match.", "status": "Shortlisted"},
            {"cand_id": "john.doe@email.com", "job_id": j_id, "score": 80.0, "reason": "Meets min YOE.", "status": "Shortlisted"},
            {"cand_id": "bob@email.com", "job_id": j_id, "score": 45.0, "reason": "Lacks YOE.", "status": "Rejected"}
        ]
        return json.dumps(mock)

    def rank(self, j_id: str) -> str:
        raw = self.get_cands(j_id)
        cands = [MatchResult.model_validate(c) for c in json.loads(raw)]
        
        cands.sort(key=lambda x: x.score, reverse=True)
        
        board = []
        for idx, c in enumerate(cands, 1):
            board.append({
                "rank": idx,
                "cand_id": c.cand_id,
                "score": c.score,
                "status": c.status
            })
            
        return json.dumps(board, indent=4)

if __name__ == "__main__":
    agent = RankAgent()
    out = agent.rank("REQ-101")
    print(out)