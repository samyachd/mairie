import { useQuery } from "@tanstack/react-query";
import { fetchLogs, fetchOcrStats, type LogsParams } from "@/app/services/logs";

export function useLogs(params?: LogsParams) {
  return useQuery({
    queryKey: ["logs", params],
    queryFn: () => fetchLogs(params),
  });
}

export function useOcrStats(params?: { limit?: number; offset?: number }) {
  return useQuery({
    queryKey: ["ocrStats", params],
    queryFn: () => fetchOcrStats(params),
  });
}
