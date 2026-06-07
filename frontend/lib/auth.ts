const API = "http://127.0.0.1:8000/api";
const TK = "talentai_token";

export interface AuthUser {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface AuthRes {
  token: string;
  user: AuthUser;
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TK);
}

export function setToken(t: string) {
  localStorage.setItem(TK, t);
}

export function clearToken() {
  localStorage.removeItem(TK);
}

export async function signup(name: string, email: string, password: string): Promise<AuthRes> {
  const res = await fetch(`${API}/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Signup failed");
  }
  const data: AuthRes = await res.json();
  setToken(data.token);
  return data;
}

export async function login(email: string, password: string): Promise<AuthRes> {
  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Login failed");
  }
  const data: AuthRes = await res.json();
  setToken(data.token);
  return data;
}

export async function fetchProfile(): Promise<AuthUser> {
  const tk = getToken();
  if (!tk) throw new Error("Not authenticated");
  const res = await fetch(`${API}/profile`, {
    headers: { Authorization: `Bearer ${tk}` },
  });
  if (!res.ok) {
    if (res.status === 401) {
      clearToken();
      throw new Error("Session expired");
    }
    throw new Error("Failed to fetch profile");
  }
  return res.json();
}
