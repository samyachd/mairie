import api from "./api";
import type { OfficeLicence } from "@/app/types";


export interface LicenceCreatePayload {
  version: string | null;
  type_licence: string | null;
  date_achat: string | null;
  fournisseur: string | null;
  clef: string | null;
  mail_activation: string | null;
}

export type LicenceUpdatePayload = LicenceCreatePayload;

export async function createLicence(
  data: LicenceCreatePayload
): Promise<OfficeLicence> {
  const response = await api.post<OfficeLicence>("/licences/", data);
  return response.data;
}

export async function deleteLicence(id: number): Promise<void> {
  await api.delete(`/licences/${id}`);
}

export async function updateLicence(
  id: number,
  data: LicenceUpdatePayload
): Promise<OfficeLicence> {
  const response = await api.put<OfficeLicence>(`/licences/${id}/`, data);
  return response.data;
}