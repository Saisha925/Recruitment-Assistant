"use client";

import { useState } from "react";
import { AuthModal } from "@/components/auth-modal";
import { Dashboard } from "@/components/dashboard";

export interface User {
  name: string;
  email: string;
  avatar: string;
}

export default function Page() {
  const [user, setUser] = useState<User | null>(null);
  const [showAuth, setShowAuth] = useState(true);

  const handleLogin = (email: string) => {
    setUser({
      name: email.split("@")[0],
      email,
      avatar: `https://api.dicebear.com/7.x/initials/svg?seed=${email}`,
    });
    setShowAuth(false);
  };

  const handleLogout = () => {
    setUser(null);
    setShowAuth(true);
  };

  if (showAuth || !user) {
    return <AuthModal onLogin={handleLogin} />;
  }

  return <Dashboard user={user} onLogout={handleLogout} />;
}
