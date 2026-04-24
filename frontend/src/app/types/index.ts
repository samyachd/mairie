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
  tag: string;
  marque: string | null;
  proprietaire: string | null;
  service: string | null;
  batiment: string | null;
  type_equipement: string | null;
  fin_garantie: string | null; // dates en string (ISO) côté JSON
  date_achat: string | null;
  fournisseur: string | null;
  created_at: string;
  updated_at: string;
}

// ────────── Ordinateur ──────────

export interface Ordinateur extends BaseEquipment {
  office_license_id: number | null;
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
  ordinateur_id: number | null;
  slot: number | null;
}

// ────────── Licence Office ──────────

export interface OfficeLicence {
  id: number;
  version: string;
  type_licence: string | null;
  numero_bc: string;
  achat: string; // date ISO
}

// ────────── Documents (on posera les détails plus tard) ──────────

// On met des placeholders pour l'instant, on étoffera quand tu partageras
// les schémas Pydantic de Devis / BonDeCommande / Facture
export interface Devis {
  id: number;
  // TODO: compléter
}

export interface BonDeCommande {
  id: number;
  // TODO: compléter
}

export interface Facture {
  id: number;
  // TODO: compléter
}

// ────────── Réponse de /inventaire ──────────

export interface InventaireResponse {
  ordinateurs: Ordinateur[];
  ecrans: Ecran[];
  licenses: OfficeLicence[]; // attention : "licenses" au pluriel anglais côté backend
  devis: Devis[];
  bons_de_commande: BonDeCommande[];
  factures: Facture[];
}