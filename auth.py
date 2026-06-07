import os
import sqlite3
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter(prefix="/api")

DB = os.getenv("DATABASE_URL", "data/recruitment.db")
SECRET = os.getenv("JWT_SECRET", "talentai_dev_secret_k3y_2024")
ALG = "HS256"
EXP_HRS = 24

sec = HTTPBearer()


def init_users():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'recruiter'
        )
    """)
    conn.commit()
    conn.close()


def mk_token(uid: int, email: str, name: str, role: str) -> str:
    payload = {
        "sub": uid,
        "email": email,
        "name": name,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=EXP_HRS),
    }
    return jwt.encode(payload, SECRET, algorithm=ALG)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=[ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user(creds: HTTPAuthorizationCredentials = Depends(sec)) -> dict:
    return decode_token(creds.credentials)


class SignupReq(BaseModel):
    name: str
    email: str
    password: str


class LoginReq(BaseModel):
    email: str
    password: str


@router.post("/signup")
async def signup(req: SignupReq):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = ?", (req.email,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode()
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (req.name, req.email, hashed),
    )
    conn.commit()
    uid = cur.lastrowid
    conn.close()
    token = mk_token(uid, req.email, req.name, "recruiter")
    return {"token": token, "user": {"id": uid, "name": req.name, "email": req.email, "role": "recruiter"}}


@router.post("/login")
async def login(req: LoginReq):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, password_hash, role FROM users WHERE email = ?", (req.email,))
    row = cur.fetchone()
    conn.close()
    if not row or not bcrypt.checkpw(req.password.encode(), row[3].encode()):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = mk_token(row[0], row[2], row[1], row[4])
    return {"token": token, "user": {"id": row[0], "name": row[1], "email": row[2], "role": row[4]}}


@router.get("/profile")
async def profile(u: dict = Depends(get_user)):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, role FROM users WHERE id = ?", (u["sub"],))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row[0], "name": row[1], "email": row[2], "role": row[3]}
