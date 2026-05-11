import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchTables, createTable, fetchColumns, addColumn, renameColumn, dropColumn, type AddColumnPayload, type CreateTablePayload } from "@/app/services/schema";

export function useTables() {
  return useQuery({
    queryKey: ["schema", "tables"],
    queryFn: fetchTables,
  });
}

export function useCreateTable() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateTablePayload) => createTable(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["schema", "tables"] }),
  });
}

export function useColumns(table: string) {
  return useQuery({
    queryKey: ["schema", table],
    queryFn: () => fetchColumns(table),
  });
}

export function useAddColumn(table: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AddColumnPayload) => addColumn(table, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["schema", table] }),
  });
}

export function useRenameColumn(table: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ column, newName }: { column: string; newName: string }) =>
      renameColumn(table, column, newName),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["schema", table] }),
  });
}

export function useDropColumn(table: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (column: string) => dropColumn(table, column),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["schema", table] }),
  });
}
