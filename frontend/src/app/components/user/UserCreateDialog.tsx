import { useState } from "react";
import { Plus } from "lucide-react";
import { toast } from "sonner";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/app/components/ui/dialog";
import { Button } from "@/app/components/ui/button";
import { UserForm } from "./UserForm";
import { useCreateUser } from "@/app/hooks/useUser";

export function UserCreateDialog() {
  const [open, setOpen] = useState(false);
  const createMutation = useCreateUser();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nouveau
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nouvel utilisateur</DialogTitle>
        </DialogHeader>
        <UserForm
          isPending={createMutation.isPending}
          onSubmit={(data) => {
            createMutation.mutate(data as Parameters<typeof createMutation.mutate>[0], {
              onSuccess: () => { setOpen(false); toast.success("Utilisateur créé"); },
              onError: (e: unknown) => {
                const msg = (e as { response?: { data?: { detail?: string | { erreurs?: string[] } } } })?.response?.data?.detail;
                if (msg && typeof msg === "object" && msg.erreurs) {
                  toast.error(msg.erreurs.join(" · "));
                } else {
                  toast.error(typeof msg === "string" ? msg : "Erreur lors de la création");
                }
              },
            });
          }}
        />
      </DialogContent>
    </Dialog>
  );
}
