import api from "./api";
import type { BonDeCommande, Ordinateur } from "@/app/types";


export interface BonDeCommandeCreatePayload {
    path: string;          // format ISO "YYYY-MM-DD"
}

export type BonDeCommandeUpdatePayload = BonDeCommandeCreatePayload;

export async function createBonDeCommande(
  data: BonDeCommandeCreatePayload
): Promise<BonDeCommande> {
  const response = await api.post<BonDeCommande>("/bons-de-commande/", data);
  return response.data;
}

export async function deleteBonDeCommande(id: number): Promise<void> {
  await api.delete(`/bons-de-commande/${id}`);
}

export async function updateBonDeCommande(
  id: number,
  data: BonDeCommandeUpdatePayload
): Promise<BonDeCommande> {
  const response = await api.put<BonDeCommande>(`/bons-de-commande/${id}/`, data);
  return response.data;
}

