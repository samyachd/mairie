import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createOrdinateur, deleteOrdinateur, OrdinateurUpdatePayload, updateOrdinateur } from "@/app/services/ordinateur";

export function useDeleteOrdinateur() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteOrdinateur,
    onSuccess: () => {
      // Invalide le cache de /inventaire → refetch automatique
      queryClient.invalidateQueries({ queryKey: ["inventaire"] });
    },
  });
}

export function useCreateOrdinateur() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createOrdinateur,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventaire"] });
    },
  });
}

export function useUpdateOrdinateur() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: OrdinateurUpdatePayload }) =>
      updateOrdinateur(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventaire"] });
    },
  });
}