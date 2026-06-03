import sqlite3
import os
import json

DB_PATH = os.getenv("DATABASE_URL", "data/recruitment.db")

def seed():
    # 1. Ensure the 'data' folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    curr = conn.cursor()
    
    # 2. FOOLPROOF FIX: Create the jobs table right here if it doesn't exist
    curr.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            skills TEXT,
            min_yoe REAL
        )
    """)
    
    # 3. Define our two open requisitions
    jobs = [
        ("REQ-101", "AI/ML Engineer", json.dumps(["Python", "C++", "Machine Learning"]), 2.0),
        ("REQ-102", "Data Scientist", json.dumps(["Python", "Machine Learning", "NLP", "LLMs"]), 0.5)
    ]
    
    # 4. Insert them into the jobs table
    curr.executemany("""
        INSERT OR REPLACE INTO jobs (id, title, skills, min_yoe)
        VALUES (?, ?, ?, ?)
    """, jobs)
    
    conn.commit()
    conn.close()
    print("✅ Database successfully created and seeded with Job Requisitions!")

if __name__ == "__main__":
    seed()