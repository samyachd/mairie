import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,  // ← l'URL de ton backend
});

export default api;