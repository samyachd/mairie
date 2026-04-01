import { createContext, useState, useEffect } from "react";
import { getInventaire } from "../services/calls";
import { Equipement } from "../types/index";

const [equipements, setEquipements] = useState<Equipement[]>([]);

// Au chargement — un seul appel API
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