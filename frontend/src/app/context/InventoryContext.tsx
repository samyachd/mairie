import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useAuth } from "@/app/hooks/useAuth";
import { getInventaire } from "@/app/services/getInventaire";
import { Equipement } from "@/app/types/index";

interface InventoryContextType {
  // Auth
  token: string | null;
  isAuthenticated: boolean;
  login: (credentials: { username: string; password: string }) => Promise<void>;
  logout: () => void;
  
  // Inventaire
  equipements: Equipement[];
  ordinateurs: Equipement[];
  ecrans: Equipement[];
  licences: Equipement[];
}

const InventoryContext = createContext<InventoryContextType | null>(null);

export function InventoryProvider({ children }: { children: ReactNode }) {
  const auth = useAuth();
  
  // ─── Inventaire ─────────────────────────────────────
  const [equipements, setEquipements] = useState<Equipement[]>([]);
  
  useEffect(() => {
    // On ne fetch que si l'utilisateur est connecté
    if (!auth.isAuthenticated) return;
    
    const fetchData = async () => {
      try {
        const data = await getInventaire();
        setEquipements(data);
      } catch (error) {
        console.error("Erreur lors du fetch de l'inventaire :", error);
      }
    };
    
    fetchData();
  }, [auth.isAuthenticated]);
  
  // Filtrage par catégorie
  const ordinateurs = equipements.filter(e => e.type === "ordinateur");
  const ecrans = equipements.filter(e => e.type === "ecran");
  const licences = equipements.filter(e => e.type === "licence");
  
  // ─── Valeur du contexte ─────────────────────────────
  const value: InventoryContextType = {
    ...auth,
    equipements,
    ordinateurs,
    ecrans,
    licences,
  };
  
  return (
    <InventoryContext.Provider value={value}>
      {children}
    </InventoryContext.Provider>
  );
}

export const useInventory = () => {
  const context = useContext(InventoryContext);
  if (!context) throw new Error("useInventory doit être utilisé dans InventoryProvider");
  return context;
};