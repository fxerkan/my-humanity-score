"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { setTokens } from "@/lib/auth";
import { useAuthStore } from "@/store/authStore";

interface LoginResponse {
  access_token: string;
  refresh_token: string;
}

interface MeResponse {
  id: string;
  username: string;
  email: string;
  display_name: string | null;
  avatar_url: string | null;
}

const DEMO_USERS = [
  { name: "Elif Kaya",       email: "elif@demo.mhs",   password: "Demo1234!", score: "342" },
  { name: "Marcus Johnson",  email: "marcus@demo.mhs",  password: "Demo1234!", score: "438" },
  { name: "Yuna Park",       email: "yuna@demo.mhs",    password: "Demo1234!", score: "305" },
  { name: "Amir Hassan",     email: "amir@demo.mhs",    password: "Demo1234!", score: "378" },
  { name: "Sofia Rossi",     email: "sofia@demo.mhs",   password: "Demo1234!", score: "392" },
];

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const tokens = await apiFetch<LoginResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setTokens(tokens.access_token, tokens.refresh_token);
      const me = await apiFetch<MeResponse>("/users/me");
      login(me, tokens.access_token, tokens.refresh_token);
      const params = new URLSearchParams(window.location.search);
      router.push(params.get("next") ?? "/feed");
    } catch {
      setError("Invalid email or password. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function fillDemo(u: (typeof DEMO_USERS)[number]) {
    setEmail(u.email);
    setPassword(u.password);
    setError(null);
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-bg-dark px-4 py-8">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white">Sign in</h1>
          <p className="text-slate-400 text-sm mt-1">My Humanity Score</p>
        </div>

        {/* Demo accounts */}
        <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 space-y-2">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide">
            Demo accounts — click to fill
          </p>
          <div className="space-y-1">
            {DEMO_USERS.map((u) => (
              <button
                key={u.email}
                type="button"
                onClick={() => fillDemo(u)}
                className="w-full text-left flex items-center justify-between rounded-lg px-3 py-1.5 hover:bg-slate-700 transition-colors group"
              >
                <span className="text-sm text-slate-300 group-hover:text-white">{u.name}</span>
                <span className="text-xs text-angel-gold font-semibold">MHS {u.score}</span>
              </button>
            ))}
          </div>
          <p className="text-xs text-slate-500">Password for all: <code className="text-slate-400">Demo1234!</code></p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-slate-400 mb-1" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-angel-gold"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="block text-sm text-slate-400 mb-1" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-angel-gold"
              placeholder="••••••••"
            />
          </div>

          {error && <p className="text-crisis-red text-sm">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-angel-gold px-4 py-2 font-semibold text-slate-900 hover:bg-yellow-400 disabled:opacity-50 transition-colors"
          >
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="text-center text-sm text-slate-400">
          No account?{" "}
          <Link href="/register" className="text-angel-gold hover:underline">
            Register
          </Link>
        </p>
      </div>
    </main>
  );
}
