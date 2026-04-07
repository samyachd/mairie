import { useState, useEffect } from "react";
import type { Credentials } from "@/app/types/index";
import { loginService } from "@/app/services/auth";
import api from "@/app/services/api";

export function useAuth() {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );

  const isAuthenticated = token !== null;

  useEffect(() => {
    if (token) {
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      localStorage.setItem("token", token);
    } else {
      delete api.defaults.headers.common["Authorization"];
      localStorage.removeItem("token");
    }
  }, [token]);

  const login = async (credentials: Credentials) => {
    const data = await loginService(credentials);
    setToken(data.access_token);
  };

  const logout = () => setToken(null);

  return { token, isAuthenticated, login, logout };
}