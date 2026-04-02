import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useAuth } from "@/app/hooks/useAuth";
import { getInventaire } from "@/app/services/getInventaire";
import { Equipement } from "@/app/types/index";

interface InventoryContextType {
  token: string | null;
  isAuthenticated: boolean;
  login: (credentials: { username: string; password: string }) => Promise<void>;
  logout: () => void;
}

const InventoryContext = createContext<InventoryContextType | null>(null);

export function InventoryProvider({ children }: { children: ReactNode }) {
  const auth = useAuth();  // ← toute la logique vient du hook

  return (
    <InventoryContext.Provider value={auth}>
      {children}        // ← toute l'app a accès à auth
    </InventoryContext.Provider>
  );
}

export const useInventory = () => {
  const context = useContext(InventoryContext);
  if (!context) throw new Error("useInventory doit être utilisé dans InventoryProvider");
  return context;
};

//_______________________________________________________________________//

const [equipements, setEquipements] = useState<Equipement[]>([]);

// Au chargement — un seul appel API pour récupérer tout les équipements
useEffect(() => {
  const fetchData = async () => {
    const data = await getInventaire();
    setEquipements(data);
  };

  fetchData();
}, []);

// Les catégories se calculent automatiquement depuis les données
const ordinateurs = equipements.filter(e => e.type === "ordinateur");
const ecrans      = equipements.filter(e => e.type === "ecran");
const licences    = equipements.filter(e => e.type === "licence");