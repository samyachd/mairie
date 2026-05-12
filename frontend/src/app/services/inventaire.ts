import api from "./api";
import type { InventaireResponse } from "@/app/types";

export async function fetchInventaire(): Promise<InventaireResponse> {
  const response = await api.get<InventaireResponse>("/inventaire");
  return response.data;
}