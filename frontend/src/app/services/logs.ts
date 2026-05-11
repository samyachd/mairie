import api from "./api";

export interface LogEntry {
  id: number;
  user_id: number | null;
  timestamp: string;
  action: string;
  table_cible: string;
  item_id: number | null;
  detail: string | null;
}

export interface OcrStat {
  id: number;
  user_id: number;
  timestamp: string;
  nom_fichier: string;
  type_document: string;
  type_mime: string;
  taille_fichier: number;
  nb_pages: number;
  nb_champs_extraits: number;
  nb_champs_vides: number;
  taux_completude: number;
  duree_ms: number;
  duree_ocr_ms: number;
  duree_extraction_ms: number;
  succes: boolean;
  resultat_json: string | null;
}

export interface LogsParams {
  action?: string;
  table_cible?: string;
  user_id?: number;
  limit?: number;
  offset?: number;
}

export async function fetchLogs(params?: LogsParams): Promise<LogEntry[]> {
  const response = await api.get<LogEntry[]>("/logs/", { params });
  return response.data;
}

export async function fetchOcrStats(params?: { limit?: number; offset?: number }): Promise<OcrStat[]> {
  const response = await api.get<OcrStat[]>("/logs/ocr", { params });
  return response.data;
}

export async function restoreLog(logId: number): Promise<void> {
  await api.post(`/logs/${logId}/restore`);
}
