import { RouterProvider } from "react-router";
import { router } from "@/app/routes";
import { InventoryProvider } from "@/app/context/InventoryContext";

export default function App() {
  return (
    <InventoryProvider>
      <RouterProvider router={router} />
    </InventoryProvider>
  );
}
