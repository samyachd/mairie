import { createBrowserRouter } from "react-router";
import { Dashboard } from "@/app/pages/Dashboard";
import { Products } from "@/app/pages/Products";
import { AddProduct } from "@/app/pages/AddProduct";
import { EditProduct } from "@/app/pages/EditProduct";
import { Layout } from "@/app/components/Layout";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: Dashboard },
      { path: "products", Component: Products },
      { path: "products/add", Component: AddProduct },
      { path: "products/edit/:id", Component: EditProduct },
    ],
  },
]);
