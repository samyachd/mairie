import { RouterProvider } from "react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { router } from "./routes";
import { useAuth } from "./hooks/useAuth";
import { setUnauthorizedHandler } from "./services/api";
import { Toaster } from "./components/ui/sonner";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      refetchOnWindowFocus: false,
    },
  },
});

// On 401, log out through the store — keeps axios header, localStorage
// and isAuthenticated in sync, which a window.location reload would not.
setUnauthorizedHandler(() => useAuth.getState().logout());

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <Toaster />
    </QueryClientProvider>
  );
}