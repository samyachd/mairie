import api from "./api";

export const getInventaire = async () => {
  const response = await api.get("/inventaire");
  return response.data;  // liste plate de tous les équipements
}