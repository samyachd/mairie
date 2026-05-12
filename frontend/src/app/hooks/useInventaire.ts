import { useQuery } from "@tanstack/react-query";
import { fetchInventaire } from "@/app/services/inventaire";

export function useInventaire() {
  return useQuery({
    queryKey: ["inventaire"],
    queryFn: fetchInventaire,
  });
}