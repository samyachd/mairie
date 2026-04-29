// components/OrdinateurEditDialog.tsx
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/app/components/ui/dialog";
import { OrdinateurForm } from "./OrdinateurForm";
import { useUpdateOrdinateur } from "@/app/hooks/useOrdinateur";
import type { Agent, Ordinateur } from "@/app/types";

interface Props {
  ordinateur: Ordinateur;
  agents: Agent[];
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function OrdinateurEditDialog({
  ordinateur,
  agents,
  open,
  onOpenChange,
}: Props) {
  const updateMutation = useUpdateOrdinateur();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Modifier {ordinateur.nom_reseau}</DialogTitle>
          <DialogDescription>
            Modifiez les informations de l'ordinateur. Les champs non modifiés
            conservent leur valeur actuelle.
          </DialogDescription>
        </DialogHeader>
        <OrdinateurForm
          agents={agents}
          isPending={updateMutation.isPending}
          submitLabel="Enregistrer les modifications"
          defaultValues={{
            nom_reseau: ordinateur.nom_reseau,
            marque: ordinateur.marque,
            date_achat: ordinateur.date_achat,
            proprietaire: ordinateur.proprietaire,
            service: ordinateur.service,
            agent_id: ordinateur.agent_id,
          }}
          onSubmit={(data) => {
            updateMutation.mutate(
              { id: ordinateur.id, data },
              {
                onSuccess: () => {
                  onOpenChange(false);
                },
              }
            );
          }}
        />
      </DialogContent>
    </Dialog>
  );
}