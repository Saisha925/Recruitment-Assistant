import json
import os
import sqlite3

class RankAgent:
    def __init__(self):
        self.db_path = os.getenv("DATABASE_URL", "data/recruitment.db")

    def rank(self, j_id: str) -> str:
        # 1. Connect to the database and pull all evaluated candidates
        conn = sqlite3.connect(self.db_path)
        curr = conn.cursor()
        
        # Order them by score, highest to lowest
        curr.execute("SELECT id, score, status FROM candidates ORDER BY score DESC")
        rows = curr.fetchall()
        conn.close()
        
        # 2. Format them for the UI Leaderboard
        board = []
        for idx, row in enumerate(rows, 1):
            board.append({
                "rank": idx,
                "cand_id": row[0],
                "score": row[1],
                "status": row[2]
            })
            
        return json.dumps(board, indent=4)