import { toast } from "sonner";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/app/components/ui/dialog";
import { UserForm } from "./UserForm";
import { useUpdateUser } from "@/app/hooks/useUser";
import type { UserRecord } from "@/app/services/user";

interface Props {
  user: UserRecord;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function UserEditDialog({ user, open, onOpenChange }: Props) {
  const updateMutation = useUpdateUser();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Modifier l'utilisateur</DialogTitle>
        </DialogHeader>
        <UserForm
          isEdit
          isPending={updateMutation.isPending}
          defaultValues={{ nom: user.nom, email: user.email, role: user.role }}
          onSubmit={(data) => {
            updateMutation.mutate({ id: user.id, data }, {
              onSuccess: () => { onOpenChange(false); toast.success("Utilisateur mis à jour"); },
              onError: (e: unknown) => {
                const msg = (e as { response?: { data?: { detail?: string | { erreurs?: string[] } } } })?.response?.data?.detail;
                if (msg && typeof msg === "object" && msg.erreurs) {
                  toast.error(msg.erreurs.join(" · "));
                } else {
                  toast.error(typeof msg === "string" ? msg : "Erreur lors de la mise à jour");
                }
              },
            });
          }}
        />
      </DialogContent>
    </Dialog>
  );
}
