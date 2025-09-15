import { useState } from "react";
import { useAuthContext } from "../contexsts/AuthContext";
import type { userRegisterData } from "../types/auth";
import Navbar from "../components/Navbar";
import { Navigate } from "react-router-dom";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const authCtx = useAuthContext();

  if (authCtx.user) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="flex flex-col h-screen bg-background font-sans">
      <header>
        <Navbar />
      </header>

      <main className="flex pt-[20vh] justify-center text-background">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const registerData: userRegisterData = {
              email: email,
              username: username,
              password: password,
            };
            authCtx.register(registerData);
          }}
          className="flex flex-col gap-4"
        >
          <div className="flex flex-col gap-1">
            <label
              htmlFor="email"
              className="text-sm text-foreground font-bold"
            >
              E-mail
            </label>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.currentTarget.value)}
              className="bg-foreground hover:bg-gray-400 rounded-xl box-border px-2 py-1 border-2 border-transparent focus:outline-none focus:border-accent"
              placeholder="E-mail"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label
              htmlFor="username"
              className="text-sm text-foreground font-bold"
            >
              Username
            </label>
            <input
              value={username}
              onChange={(event) => setUsername(event.currentTarget.value)}
              className="bg-foreground hover:bg-gray-400 rounded-xl box-border px-2 py-1 border-2 border-transparent focus:outline-none focus:border-accent"
              placeholder="Username"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label
              htmlFor="password"
              className="text-sm text-foreground font-bold"
            >
              Password
            </label>
            <input
              value={password}
              onChange={(event) => setPassword(event.currentTarget.value)}
              className="bg-foreground hover:bg-gray-400 rounded-xl box-border px-2 py-1 border-2 border-transparent focus:outline-none focus:border-accent"
              placeholder="Password"
              type="password"
            />
          </div>
          <button
            type="submit"
            className="bg-primary hover:bg-primary-dark text-white py-2 px-4 rounded-4xl cursor-pointer"
          >
            Create account
          </button>
        </form>
      </main>
    </div>
  );
}
