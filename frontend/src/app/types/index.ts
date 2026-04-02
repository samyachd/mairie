export interface Equipement {
  id: number;
  nom: string;
  type: "ordinateur" | "ecran" | "licence";
  // ... autres champs
}

export interface LoginResponse {
  access_token: string;
}

export interface Credentials {
  username: string;
  password: string;
}

export interface User {
  id: number;
  email: string;
  role: "admin" | "lecteur";
}