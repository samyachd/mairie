import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Credentials } from "@/app/types/index";
import { loginService } from "@/app/services/auth";
import api from "@/app/services/api";

interface AuthState {
  token: string | null;
  role: string | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

function parseJwtRole(token: string): string | null {
  try {
    return (JSON.parse(atob(token.split(".")[1])) as { role?: string }).role ?? null;
  } catch {
    return null;
  }
}

function applyAuthHeader(token: string | null) {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      role: null,
      isAuthenticated: false,

      login: async (credentials) => {
        const data = await loginService(credentials);
        applyAuthHeader(data.access_token);
        set({ token: data.access_token, role: parseJwtRole(data.access_token), isAuthenticated: true });
      },

      logout: () => {
        applyAuthHeader(null);
        set({ token: null, role: null, isAuthenticated: false });
      },
    }),
    {
      name: "auth",
      partialize: (state) => ({ token: state.token }),
      onRehydrateStorage: () => (state) => {
        if (state?.token) {
          applyAuthHeader(state.token);
          state.isAuthenticated = true;
          state.role = parseJwtRole(state.token);
        }
      },
    }
  )
);
