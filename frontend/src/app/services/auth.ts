import api from "./api";
import { LoginResponse } from "@/app/types/index";
import { Credentials } from "@/app/types/index";

export const loginService = async (credentials: Credentials): Promise<LoginResponse> => {
  const response = await api.post("/auth/login", credentials);
  return response.data as LoginResponse;  // { access_token: "..." }
};