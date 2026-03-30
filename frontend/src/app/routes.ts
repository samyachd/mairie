import { createBrowserRouter } from "react-router";
import { Login } from "@/app/pages/Login";
import { Inventaire } from "@/app/pages/Inventaire";
import { Gestion } from "@/app/pages/Gestion";
import { Parametres } from "@/app/pages/Parametres";
import { Admin } from "@/app/pages/Adminstration";
import { Layout } from "@/app/components/Layout";

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