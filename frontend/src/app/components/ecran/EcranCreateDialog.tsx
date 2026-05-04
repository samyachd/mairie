import { useState } from "react";
import { Plus } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/app/components/ui/dialog";
import { Button } from "@/app/components/ui/button";
import { EcranForm } from "./EcranForm";
import { useCreateEcran } from "@/app/hooks/useEcran";
import type { Agent } from "@/app/types";

interface Props {
  agents: Agent[];
}

export function EcranCreateDialog({ agents }: Props) {
  const [open, setOpen] = useState(false);
  const createMutation = useCreateEcran();

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
          <DialogTitle>Nouvel écran</DialogTitle>
          <DialogDescription>
            Saisissez les informations de base. Le slot et l'ordinateur lié
            peuvent être renseignés après création.
          </DialogDescription>
        </DialogHeader>
        <EcranForm
          agents={agents}
          isPending={createMutation.isPending}
          onSubmit={(data) => {
            createMutation.mutate(data, {
              onSuccess: () => setOpen(false),
            });
          }}
        />
      </DialogContent>
    </Dialog>
  );
}
