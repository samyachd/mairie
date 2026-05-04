import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/app/components/ui/dialog";
import { EcranForm } from "./EcranForm";
import { useUpdateEcran } from "@/app/hooks/useEcran";
import type { Agent, Ecran } from "@/app/types";

interface Props {
  ecran: Ecran;
  agents: Agent[];
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function EcranEditDialog({
  ecran,
  agents,
  open,
  onOpenChange,
}: Props) {
  const updateMutation = useUpdateEcran();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            Modifier {ecran.tag ?? `écran #${ecran.id}`}
          </DialogTitle>
          <DialogDescription>
            Modifiez les informations de l'écran.
          </DialogDescription>
        </DialogHeader>
        <EcranForm
          agents={agents}
          isPending={updateMutation.isPending}
          submitLabel="Enregistrer les modifications"
          defaultValues={{
            taille: ecran.taille,
            marque: ecran.marque,
            date_achat: ecran.date_achat,
            proprietaire: ecran.proprietaire,
            service: ecran.service,
            agent_id: ecran.agent_id,
          }}
          onSubmit={(data) => {
            updateMutation.mutate(
              { id: ecran.id, data },
              {
                onSuccess: () => onOpenChange(false),
              }
            );
          }}
        />
      </DialogContent>
    </Dialog>
  );
}
