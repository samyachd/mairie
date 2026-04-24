// src/app/App.tsx
import { RouterProvider } from "react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { router } from "./routes";

// On crée UN SEUL QueryClient pour toute l'app (singleton)
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,       // données fraîches pendant 1 minute
      refetchOnWindowFocus: false, // pas de refetch quand on revient sur l'onglet
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}