import { createBrowserRouter } from "react-router";
import { Layout } from "./components/Layout";
import { Login } from "./pages/Login";
import { Inventaire } from "./pages/Inventaire";
import { Gestion } from "./pages/Gestion";
import { Parametres } from "./pages/Parametres";
import { Administration } from "./pages/Administration";
import { ProtectedRoute } from "./routes/ProtectedRoute";

export const router = createBrowserRouter([
  {
    path: "/login",
    Component: Login,
  },
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <Layout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, Component: Inventaire },
      { path: "gestion", Component: Gestion },
      { path: "administration", Component: Administration },
      { path: "parametres", Component: Parametres },
    ],
  },
]);
