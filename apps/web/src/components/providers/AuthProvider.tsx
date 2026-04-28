"use client";

import { useEffect } from "react";
import { apiFetch } from "@/lib/api";
import { getAccessToken, getRefreshToken, clearTokens } from "@/lib/auth";
import { useAuthStore, type AuthUser } from "@/store/authStore";

/**
 * AuthProvider — on mount, restores the authenticated user from a persisted
 * access token (localStorage) so page refreshes don't force re-login.
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { user, login, logout, setLoading } = useAuthStore();

  useEffect(() => {
    if (user) return; // already hydrated

    const token = getAccessToken();
    if (!token) return;

    setLoading(true);
    apiFetch<AuthUser>("/users/me")
      .then((me) => {
        login(me, token, getRefreshToken() ?? "");
      })
      .catch(() => {
        clearTokens();
        logout();
      })
      .finally(() => setLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return <>{children}</>;
}
