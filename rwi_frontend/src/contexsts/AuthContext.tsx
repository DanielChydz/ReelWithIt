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

  useEffect(() => {
    async function tryRefresh(): Promise<void> {
      try {
        const res = await fetch("/auth/refresh", {
          method: "POST",
          credentials: "include",
        });

        if (!res.ok) {
          setAccessToken(null);
          setUser(null);
        }

        const loginData = await res.json();
        setAccessToken(loginData.accessToken);

        const userRes = await fetch("user/me", {
          headers: { Authorization: `Bearer ${loginData.accessToken}` },
        });

        if (!userRes.ok) {
          setUser(null);
        }

        const userData = await userRes.json();
        setUser(userData);
      } catch (err) {
        setAccessToken(null);
        setUser(null);
      }
    }

    tryRefresh();
  }, []);

  async function register(user: userRegisterData): Promise<void> {
    const res = await fetch("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: JSON.stringify({
        email: user.email,
        username: user.username,
        password: user.password,
      }),
    });

    if (!res.ok) {
      throw new Error("Registration failed");
    }

    logIn(user);
  }

  async function logIn(user: userLoginData): Promise<void> {
    const res = await fetch("/auth/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      credentials: "include",
      body: JSON.stringify({ username: user.email, password: user.password }),
    });

    if (!res.ok) {
      throw new Error("Login failed");
    }

    const loginDataRes = await res.json();
    setAccessToken(loginDataRes.accessToken);

    const userRes = await fetch("user/me", {
      headers: { Authorization: `Bearer ${loginDataRes.accessToken}` },
    });

    if (!userRes.ok) {
      throw new Error("Could not fetch user data");
    }

    const userData = await userRes.json();
    setUser(userData);
  }

  async function logOut(): Promise<void> {
    const res = await fetch("/auth/logout", {
      method: "POST",
      credentials: "include",
    });

    if (!res.ok) {
      throw new Error("Logout failed");
    }

    setAccessToken("");
    setUser(null);
    window.location.reload();
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
