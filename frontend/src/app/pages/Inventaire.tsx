// src/app/pages/Inventaire.tsx
import { useInventaire } from "@/app/hooks/useInventaire";

export function Inventaire() {
  const { data, isLoading, isError, error } = useInventaire();

  if (isLoading) {
    return <div className="p-6">Chargement...</div>;
  }

  if (isError) {
    return (
      <div className="p-6">
        Erreur : {error instanceof Error ? error.message : "inconnue"}
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Inventaire</h1>
      <pre className="bg-gray-100 p-4 rounded text-xs overflow-auto">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}