import api from "./api";

export const loginService = async (username: string, password: string) => {
  const response = await api.post("/auth/login", { username, password });
  return response.data;  // { access_token: "..." }
};