import React, { createContext, useContext, useEffect, useState } from "react";
import type {
  userData,
  userLoginData,
  userRegisterData,
  AuthContextType,
} from "../types/auth";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<userData | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  // load cached user before refreshing
  const cached = localStorage.getItem("user");
  if (user === null && cached !== null) {
    try {
      const parsed = JSON.parse(cached) as userData;
      setUser(parsed);
    } catch {
      localStorage.removeItem("user");
    }
  }

  useEffect(() => {
    async function fetchUser() {}

    async function tryRefresh(): Promise<void> {
      try {
        const res = await fetch("http://localhost:8000/auth/refresh", {
          method: "POST",
          credentials: "include",
        });

        if (!res.ok) {
          setAccessToken(null);
          setUser(null);
          return;
        }

        const loginData = await res.json();
        setAccessToken(loginData.token);

        const userRes = await fetch("http://localhost:8000/user/me", {
          headers: { Authorization: `Bearer ${loginData.token}` },
        });

        if (!userRes.ok) {
          setUser(null);
          return;
        }

        const userData = await userRes.json();
        if (userData.detail != "Could not validate credentials") {
          setUser(userData);
          localStorage.setItem("user", JSON.stringify(userData));
        }
      } catch (err) {
        setAccessToken(null);
        setUser(null);
        localStorage.removeItem("user");
      }
    }

    tryRefresh();
  }, []);

  async function register(user: userRegisterData): Promise<void> {
    const res = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: user.email,
        username: user.username,
        password: user.password,
      }),
    });

    if (!res.ok) {
      throw new Error("Registration failed");
    }

    const loginData: userLoginData = {
      email: user.email,
      password: user.password,
    };

    logIn(loginData);
  }

  async function logIn(user: userLoginData): Promise<void> {
    const res = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      credentials: "include",
      body: new URLSearchParams({
        username: user.email,
        password: user.password,
      }),
    });

    if (!res.ok) {
      throw new Error("Login failed");
    }

    const loginDataRes = await res.json();
    setAccessToken(loginDataRes.token);

    const userRes = await fetch("http://localhost:8000/user/me", {
      headers: { Authorization: `Bearer ${loginDataRes.token}` },
    });

    if (!userRes.ok) {
      setUser(null);
    }

    const userData = await userRes.json();
    if (userData.detail != "Could not validate credentials") {
      setUser(userData);
      localStorage.setItem("user", JSON.stringify(userData));
    }
  }

  async function logOut(): Promise<void> {
    const res = await fetch("http://localhost:8000/auth/logout", {
      method: "POST",
      credentials: "include",
    });

    if (!res.ok) {
      throw new Error("Logout failed");
    }

    setAccessToken("");
    setUser(null);
    localStorage.removeItem("user");
  }

  return (
    <AuthContext.Provider
      value={{ user, accessToken, logIn, logOut, register }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuthContext must be used within AuthProvider");
  }
  return ctx;
}
