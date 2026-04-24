import { useState } from "react";
import { useNavigate } from "react-router";
import { useAuth } from "../hooks/useAuth";

export function Login() {

  // Récupère la fonction login du contexte
  const { login } = useAuth();
  // Permet de rediriger après login
  const navigate = useNavigate();

  // credentials pour login
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });

  // Pour afficher une erreur si login échoue
  const [error, setError] = useState<string | null>(null);
  // Pour désactiver le bouton pendant la requête
  const [loading, setLoading] = useState(false);

  // Appelle le contexte UseInventory et la fonction login du contexte
  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      await login(credentials);
      navigate("/");
    } catch {
      setError("Identifiants incorrects");
    } finally {
      setLoading(false);
    }
  };

  // HTML du formulaire de login
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg border border-gray-200 w-full max-w-sm">

        <h1 className="text-xl font-semibold text-gray-900 mb-6">
          Connexion
        </h1>

        <div className="space-y-4">
          <input
            type="text"
            placeholder="Nom d'utilisateur"
            value={credentials.username}
            onChange={e => setCredentials({ ...credentials, username: e.target.value })}
            onKeyDown={e => e.key === "Enter" && handleSubmit()}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <input
            type="password"
            placeholder="Mot de passe"
            value={credentials.password}
            onChange={e => setCredentials({ ...credentials, password: e.target.value })}
            onKeyDown={e => e.key === "Enter" && handleSubmit()}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          {error && (
            <p className="text-sm text-red-600">{error}</p>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Connexion..." : "Se connecter"}
          </button>
        </div>

      </div>
    </div>
  );
}


/*Ce que chaque partie fait
credentials  → stocke username + password ensemble
error        → message d'erreur si login échoue
loading      → désactive le bouton pendant la requête

handleSubmit → appelle login() → succès : navigate("/")
                              → échec : affiche l'erreur

onKeyDown    → soumet avec la touche Entrée
finally      → remet loading à false dans tous les cas
*/