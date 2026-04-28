"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";

export function Header() {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  function handleLogout() {
    logout();
    router.push("/login");
  }

  return (
    <header className="h-14 border-b border-slate-800 bg-slate-900 flex items-center px-4 gap-4">
      <div className="flex-1" />

      {user ? (
        <div className="flex items-center gap-3">
          <Link
            href={`/u/${user.username}`}
            className="text-sm text-slate-300 hover:text-white"
          >
            {user.display_name ?? user.username}
          </Link>
          <button
            onClick={handleLogout}
            className="text-sm text-slate-400 hover:text-white"
          >
            Sign out
          </button>
        </div>
      ) : (
        <Link
          href="/login"
          className="text-sm text-slate-300 hover:text-white"
        >
          Sign in
        </Link>
      )}
    </header>
  );
}
