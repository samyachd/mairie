import api from "./api";
import type { Ordinateur } from "@/app/types";


export interface OrdinateurCreatePayload {
  nom_reseau: string | null;
  marque: string | null;
  date_achat: string | null;
  proprietaire: string | null;
  service: string | null;
  agent_id: number | null;
}

export type OrdinateurUpdatePayload = OrdinateurCreatePayload;

export async function createOrdinateur(
  data: OrdinateurCreatePayload
): Promise<Ordinateur> {
  const response = await api.post<Ordinateur>("/ordinateurs/", data);
  return response.data;
}

export async function deleteOrdinateur(id: number): Promise<void> {
  await api.delete(`/ordinateurs/${id}`);
}

export async function updateOrdinateur(
  id: number,
  data: OrdinateurUpdatePayload
): Promise<Ordinateur> {
  const response = await api.put<Ordinateur>(`/ordinateurs/${id}/`, data);
  return response.data;
}

