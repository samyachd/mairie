// src/app/types/index.ts

// ────────── Auth ──────────

export interface Credentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
}

export interface User {
  id: number;
  email: string;
  role: "admin" | "user" | "read"; // aligné sur le backend
}

// ────────── Inventaire : base commune ──────────

// Les champs communs à tous les équipements (Ordinateur, Ecran)
// Correspond à BaseEquipmentRead côté backend
export interface BaseEquipment {
  id: number;
  tag: string | null;
  marque: string | null;
  proprietaire: string | null;
  service: string | null;
  batiment: string | null;
  type_equipement: string | null;
  fournisseur: string | null;
  fin_garantie: string | null;
  date_achat: string;                 // ← obligatoire (dates en string ISO en JSON)
  created_at: string;
  updated_at: string | null;
}

// ────────── Ordinateur ──────────

export interface Ordinateur extends BaseEquipment {
  agent_id: number | null;
  officelicence_id: number | null;
  devis_id: number | null;
  bon_de_commande_id: number | null;
  facture_id: number | null;
  
  ram: string | null;
  os: string | null;
  nom_reseau: string | null;
  tag_chargeur: string | null;
  ip_address: string | null;
  mac_ethernet: string | null;
  mac_wifi: string | null;
  clef_wifi: boolean | null;
  lecteur_cd: boolean | null;
  casque: boolean | null;
  absolute_dell: boolean | null;
  watt: number | null;
}

// ────────── Écran ──────────

export interface Ecran extends BaseEquipment {
  taille: string | null;
  slot: number | null;
  
  ordinateur_id: number | null;
  agent_id: number | null;
  devis_id: number | null;
  bon_de_commande_id: number | null;
  facture_id: number | null;
}
// ────────── Licence Office ──────────

export interface OfficeLicence {
  id: number;
  version: string;
  type_licence: string | null;
  fournisseur: string | null;
  date_achat: string;
  
  devis_id: number | null;
  bon_de_commande_id: number | null;
  facture_id: number | null;
  
  created_at: string;
  updated_at: string | null;
}
// ────────── Agent ──────────
export interface Agent {
  id: number;
  nom: string;
  prenom: string;
  service: string | null;
  email: string | null;
  telephone: string | null;
  created_at: string;
  updated_at: string | null;
}


// ────────── Documents ──────────

interface DocumentBase {
  id: number;
  nom: string;
  numero: string;
  path: string;
  date_document: string;
  created_at: string;
  updated_at: string | null;
}

export interface Devis extends DocumentBase {}

export interface BonDeCommande extends DocumentBase {}

export interface Facture extends DocumentBase {
  montant_ttc: number | null;
  montant_ht: number | null;
}

// ────────── Réponse de /inventaire ──────────

export interface InventaireResponse {
  ordinateurs: Ordinateur[];
  ecrans: Ecran[];
  licences: OfficeLicence[];
  agents: Agent[];
  devis: Devis[];
  bons_de_commande: BonDeCommande[];
  factures: Facture[];
}