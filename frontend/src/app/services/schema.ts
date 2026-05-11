import api from "./api";

export interface ColumnInfo {
  name: string;
  type: string;
  nullable: boolean;
  default: string | null;
  protected: boolean;
}

export interface AddColumnPayload {
  name: string;
  type: string;
  nullable: boolean;
  default?: string | null;
}

export interface CreateTablePayload {
  name: string;
}

export const COLUMN_TYPES = [
  { value: "text",      label: "Texte" },
  { value: "integer",   label: "Entier" },
  { value: "boolean",   label: "Booléen" },
  { value: "date",      label: "Date" },
  { value: "numeric",   label: "Numérique" },
  { value: "timestamp", label: "Horodatage" },
] as const;

export async function fetchTables(): Promise<string[]> {
  const res = await api.get<string[]>("/schema/tables");
  return res.data;
}

export async function createTable(data: CreateTablePayload): Promise<void> {
  await api.post("/schema/tables", data);
}

export async function fetchColumns(table: string): Promise<ColumnInfo[]> {
  const res = await api.get<ColumnInfo[]>(`/schema/${table}`);
  return res.data;
}

export async function addColumn(table: string, data: AddColumnPayload): Promise<void> {
  await api.post(`/schema/${table}/columns`, data);
}

export async function renameColumn(table: string, column: string, newName: string): Promise<void> {
  await api.patch(`/schema/${table}/columns/${column}`, { new_name: newName });
}

export async function dropColumn(table: string, column: string): Promise<void> {
  await api.delete(`/schema/${table}/columns/${column}`);
}
