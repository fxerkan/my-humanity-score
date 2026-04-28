import { create } from "zustand";
import { clearTokens, setTokens } from "@/lib/auth";

export interface AuthUser {
  id: string;
  username: string;
  email: string;
  display_name: string | null;
  avatar_url: string | null;
}

interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  login: (user: AuthUser, accessToken: string, refreshToken: string) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: false,

  login: (user, accessToken, refreshToken) => {
    setTokens(accessToken, refreshToken);
    set({ user });
  },

  logout: () => {
    clearTokens();
    set({ user: null });
  },

  setLoading: (loading) => set({ isLoading: loading }),
}));
