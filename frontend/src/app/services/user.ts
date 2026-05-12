import api from "./api";

export interface UserRecord {
  id: number;
  nom: string;
  email: string;
  role: "admin" | "user" | "read";
}

export interface UserCreatePayload {
  nom: string;
  email: string;
  password: string;
  role: "admin" | "user" | "read";
}

export interface UserUpdatePayload {
  nom?: string;
  email?: string;
  password?: string;
  role?: "admin" | "user" | "read";
}

export async function fetchUsers(): Promise<UserRecord[]> {
  const response = await api.get<UserRecord[]>("/users/");
  return response.data;
}

export async function createUser(data: UserCreatePayload): Promise<UserRecord> {
  const response = await api.post<UserRecord>("/users/", data);
  return response.data;
}

export async function updateUser(id: number, data: UserUpdatePayload): Promise<UserRecord> {
  const response = await api.put<UserRecord>(`/users/${id}`, data);
  return response.data;
}

export async function deleteUser(id: number): Promise<void> {
  await api.delete(`/users/${id}`);
}
