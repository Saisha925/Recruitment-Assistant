"use client";

import { useState, useEffect } from "react";
import { AuthModal } from "@/components/auth-modal";
import { Dashboard } from "@/components/dashboard";
import { getToken, clearToken, fetchProfile, type AuthUser } from "@/lib/auth";

export interface User {
  name: string;
  email: string;
  avatar: string;
  role: string;
}

function toUser(au: AuthUser): User {
  return {
    name: au.name,
    email: au.email,
    avatar: `https://api.dicebear.com/7.x/initials/svg?seed=${au.email}`,
    role: au.role,
  };
}

export default function Page() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const tk = getToken();
    if (!tk) {
      setLoading(false);
      return;
    }
    fetchProfile()
      .then((au) => setUser(toUser(au)))
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  const handleLogin = (au: AuthUser) => {
    setUser(toUser(au));
  };

  const handleLogout = () => {
    clearToken();
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  if (!user) {
    return <AuthModal onLogin={handleLogin} />;
  }

  return <Dashboard user={user} onLogout={handleLogout} />;
}
