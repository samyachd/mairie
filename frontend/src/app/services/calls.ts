import axios from 'axios';

export const getInventaire = async () => {
  const response = await axios.get("/inventaire");
  return response.data;  // liste plate de tous les équipements
}