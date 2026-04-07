import { createBrowserRouter, Navigate } from "react-router";
import { ReactNode } from "react";
import { Layout } from "./components/Layout";
import { Login } from "./pages/Login";
import { Inventaire } from "./pages/Inventaire";
import { Gestion } from "./pages/Gestion";
import { Parametres } from "./pages/Parametres";
import { Administration } from "./pages/Administration";
import { useInventory } from "@/app/context/InventoryContext";

function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useInventory();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

export const router = createBrowserRouter([
  {
    path: "/login",
    Component: Login,        // ← hors du Layout, pas de sidebar
  },
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: Inventaire },
      { path: "gestion", Component: Gestion },
      { path: "administration", Component: Administration },
      { path: "parametres", Component: Parametres },
    ],
  },
]);